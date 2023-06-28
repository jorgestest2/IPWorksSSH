/*
 * IPWorks SSH 2022 C++ Edition - Sample Project
 *
 * This sample project demonstrates the usage of IPWorks SSH in a 
 * simple, straightforward way. This is not intended to be a complete 
 * application. Error handling and other checks are simplified for clarity.
 *
 * Copyright (c) 2023 /n software inc. www.nsoftware.com
 */

#include "../../include/ipworksssh.h"
#include <stdio.h>
#include <stdlib.h>
#define LINE_LEN 100

class MyCertMgr : public CertMgr
{
	//overwrite events here if needed
public:
	virtual int FireCertList(CertMgrCertListEventParams *e)
	{
		printf("%s\n", e->CertSubject);
		return 0;
	}
};

int main(int argc, char **argv)
{
	char * certStore;
	int certStoreSize;
	MyCertMgr certmgr;

	if (argv[1])
	{
		certmgr.SetCertStore(argv[1], sizeof(argv[1]));
	}
	else
	{
		certmgr.SetCertStore("MY", 2);
	}
	certmgr.GetCertStore(certStore, certStoreSize);
	printf("Listing all certificates in store %s:\n\n", certStore);

	certmgr.ListStoreCertificates();

	if (certmgr.GetLastErrorCode())
		printf("%d (%s)", certmgr.GetLastErrorCode(), certmgr.GetLastError());
	printf("\npress <return> to continue...\n");
	getchar();
	return 0;
}





