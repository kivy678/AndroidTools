#define PY_SSIZE_T_CLEAN

//////////////////////////////////////////////////////////////////////////////////

#include "elfformat.h"

#define TMP_STRING_SIZE					500

//////////////////////////////////////////////////////////////////////////////////


int GetLibraryOffset(unsigned char* 			pchBuffer,
					 Elf32_Off 					GOT_Offset,
					 struct Elf32_Sym_Linker* 	e32_sym_linker,
					 struct Elf32_Rel_Linker*	e32_rel_linker,
					 struct Elf32_GotMap_Linker* e32_gotmap_linker,
					 char*						pchGotBuffer)
{

	//////////////////////////////////////////////////////////////////////////////////

	Elf32_Word symbol_idx						= -1;
	GOT_Offset 									+= 12;

	struct Elf32_Rel_Linker* e32_rel_Node 		= e32_rel_linker;
	struct Elf32_Sym_Linker* e32_sym_Node 		= e32_sym_linker;

	unsigned int* LibraryAddress = (unsigned int*) (pchBuffer + GOT_Offset);


	struct Elf32_GotMap_Linker* e32_gotmap_Node = e32_gotmap_linker;
	struct Elf32_GotMap_Linker* e32_gotmap_NextNode = NULL;


	char* tmpStrBuffer					= (char*) malloc(sizeof(char) * TMP_STRING_SIZE);
	memset(tmpStrBuffer, 0, sizeof(char) * TMP_STRING_SIZE);

	//////////////////////////////////////////////////////////////////////////////////

	
	while (1)
	{
		symbol_idx 		= e32_rel_Node->e32_rel.getSymbol();
		e32_sym_Node 	= e32_sym_linker;

		for (int j=0; j < symbol_idx; j++)
		{
			
			e32_sym_Node = e32_sym_Node->nextPoint;
		}

		if (*LibraryAddress == 0)
		{
			break;
		}

		//printf("0x%08x %s\n", *LibraryAddress, e32_sym_Node->e32_sym_name);

		//////////////////////////////////////////////////////////////////////////////////

		e32_gotmap_Node->e32_rela = *LibraryAddress;
		e32_gotmap_Node->dynsym = e32_sym_Node->e32_sym_name;

		sprintf(tmpStrBuffer, "0x%08x %s\n", e32_gotmap_Node->e32_rela, e32_gotmap_Node->dynsym);
		strcat(pchGotBuffer, tmpStrBuffer);


		e32_gotmap_NextNode = (struct Elf32_GotMap_Linker*) malloc(sizeof(struct Elf32_GotMap_Linker));
		memset(e32_gotmap_NextNode, 0, sizeof(struct Elf32_GotMap_Linker));
		e32_gotmap_Node->nextPoint = e32_gotmap_NextNode;

		e32_gotmap_Node = e32_gotmap_NextNode;

		//////////////////////////////////////////////////////////////////////////////////

		e32_rel_Node = e32_rel_Node->nextPoint;

		LibraryAddress += 1;

	}


	//////////////////////////////////////////////////////////////////////////////////

	free(tmpStrBuffer);

	return 0;
}


Elf32_Off GetGotOffset(struct Elf32_Dyn_Linker* e32_dyn_linker)
{

	struct Elf32_Dyn_Linker* e32_dyn_Node 	= e32_dyn_linker;
	Elf32_Off GOT_Offset 					= 0;


	while(e32_dyn_Node->nextPoint != NULL)
	{
		if (strcmp(DYNAMIC_TAG[e32_dyn_Node->e32_dyn.d_tag].c_str(), "PLTGOT") == 0)
		{
			GOT_Offset = e32_dyn_Node->e32_dyn.d_un.d_ptr - 0x1000;			// align: 0x1000
			break;
		}

		e32_dyn_Node = e32_dyn_Node->nextPoint;
	}

	return GOT_Offset;
}
