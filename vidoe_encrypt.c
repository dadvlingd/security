#include<stdio.h>

unsigned char encrypt(unsigned char zdata)
{
	static char j=0;
	unsigned char i;
	unsigned char temp=0x80,temp_2=zdata;
	if (j>8)
		j=0;
	else
		j++;
	for(i=0; i<j; i++)
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
	unsigned char temp=0x80,temp_2=zdata;
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
	return temp_2;
}
int main(int argc, char **argv)
{
	unsigned char temp=0;
	unsigned long  int length=0;
	unsigned long  int already=0;
	unsigned long  int leavings=0;
	int percent =0;
	int len_temp=0;
	FILE*fp;FILE*fy;
    if(argc != 3)
    {
        printf("error, please select file \n");
        return -1;
    }
	if((fp=fopen(argv[1],"rb"))==NULL)
	{
		printf("Failed to open the file >_<\n");
	}
	else 
	{
		printf("Open the file successed !\n");
		if((fy=fopen(argv[2],"wb"))==NULL)
		{
			printf("Failed to create new file !\n");
		}
		else 
				{
			printf("create new file successed !\n");
			fseek(fp,0,SEEK_SET);
			fseek(fp,0,SEEK_END);
			length=ftell(fp);
			printf("The file total  %d  Byte\n",length);
			printf("Start encrypt...\n");
			fseek(fp,0,SEEK_SET);
			while(!feof(fp))
			{
				temp=fgetc(fp);
				temp=encrypt(temp);
				//temp=decrypt(temp);
				fputc(temp,fy);
				already++;
				//leavings=length-already;
				len_temp=(already*100)/length;
				if(len_temp>percent)
				{
					percent=len_temp;
					printf("leavings  %d  ",100-len_temp);
					putchar('%');
					putchar(10);
				}
			}
			fclose(fp);	fclose(fy);
			printf("\nwrite the file successd ! total: %d byte\n",length);
		}
	}
	getchar();
    return 0;
}
