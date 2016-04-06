#include<stdio.h>

#define ThreadNum 10

typedef struct DataBlock{
    long int stdlen; //每一块大小
    long int SplitAddr[ThreadNum]; 
}DB;

unsigned char encrypt(unsigned char zdata)
{
    static char j = 0;
    unsigned char i;
    unsigned char temp = 0x80,temp_2 = zdata;
    if (j > 8)
        j = 0;
    else
        j++;
    for(i = 0; i < j; i++)
    {
        if(zdata & temp)
        {
            temp_2 -= temp;
        }
        else 
        {
            temp_2 += temp;
        }
        temp = temp >> 1;
    }
    return temp_2;
}
unsigned char decrypt(unsigned char zdata)
{
    unsigned char i;
    unsigned char temp = 0x80,temp_2 = zdata;
    printf("zdata is %c\n", zdata);
    for(i=0; i<8; i++)
    {
        if(zdata & temp)
		{
			temp_2 -= temp;
		}
		else 
		{
			temp_2 += temp;
		}
		temp = temp >> 1;
	}
    printf("temp_2 is %c\n", temp_2);
	return temp_2;
}

//根据线程数分割成相应大小数据块 
//返回每一块的起始地址
void FileSplit(long int FileLenth)
{
    int i;
    stdlen = FileLenth / ThreadNum; 
    for(i = 0; i < ThreadNum; i++)
    {
       SplitAddr[i] = i + stdlen; 
    }
} 

//打印进度
//参数： 进度百分比 ，进度条长度
void update_process(int percent,int barlen){
    int i;
    putchar('[');
    for(i=1; i<=barlen; ++i)
        putchar(i * 100 <= percent * barlen ? '>' : ' ');
    putchar(']');
    printf("%3d%%", percent);
    for(i=0; i != barlen + 6; ++i)
        putchar('\b');
}

int main(int argc, char **argv)
{
	unsigned char temp = 0;
	long  int length = 0;
	long  int already = 0;
	int percent = 0;
	int len_temp = 0;
	FILE*fp;
    FILE*fy;
    int rc;
    if(argc != 3)
    {
        printf("error, please select file \n");
        return -1;
    }
	if((fp = fopen(argv[1], "rb")) == NULL)
	{
		printf("Failed to open the file >_<\n");
	}
	else 
	{
		printf("Open the file successed !\n");
		if((fy = fopen(argv[2], "wb")) == NULL)
		{
			printf("Failed to create new file !\n");
		}
		else 
		{
			printf("create new file successed !\n");
			fseek(fp, 0, SEEK_SET);
			fseek(fp, 0, SEEK_END);
			length = ftell(fp);
			printf("The file total  %ld  Byte\n", length);
			printf("Start encrypt...\n");
			fseek(fp, 0, SEEK_SET);
			while(!feof(fp))
			{
				rc = fgetc(fp); //reads  the next character
				temp = encrypt((unsigned char)rc);
				//temp=decrypt(temp);
				fputc(temp, fy);
				already++;
				//leavings=length-already;
				len_temp = (int)((already * 100) / length);
				if(len_temp > percent)
				{
					percent = len_temp;
                    update_process(len_temp, 50);
					//printf("%d%% done", len_temp); //百分比打印进度
                    fflush(stdout);
				}
			}
			fclose(fp);	
            fclose(fy);
			printf("\nwrite the file successd ! total: %ld byte\n", length);
		}
	}
	//getchar();
    return 0;
}
