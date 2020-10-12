#ifndef __PARSER_H__
#define __PARSER_H__


int EhrParser(unsigned char*, struct Elf32_Ehdr*, char*);
int PhrParser(unsigned char*, struct Elf32_Ehdr*, struct Elf32_Phdr*, char*);
int ShrParser(unsigned char*, struct Elf32_Ehdr*, struct Elf32_Section_Linker*, char*);
char* GetSetionName(unsigned char*, struct Elf32_Ehdr*, Elf32_Word);

int DynParser(unsigned char*, struct Elf32_Ehdr*, struct Elf32_Dyn_Linker*, char*);



#endif // __PARSER_H__
