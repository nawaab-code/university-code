#include<stdio.h>

int main()
{
    enum TV_Stations
    {
        TataSky,
        Airtel,
        Jio,
        DD
    };
    enum TV_Stations selected(TataSky);
    printf("Selected TV Station: %s", selected);
    return 0;
}