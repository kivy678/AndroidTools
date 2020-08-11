#ifndef __ELFFORMAT_H__
#define __ELFFORMAT_H__

#include "common/module.h"
#include "common/common.cpp.h"

#include "elf.h"



#define ELFFORMAT_EXCEPTION(ret, ...) 	__EXCEPTION((ret), ElfFormatException, ##__VA_ARGS__)


#ifdef __cplusplus
extern "C"
{
#endif

	extern std::map<int, std::string> FILE_TYPE;
	extern std::map<int, std::string> OBJECT_FILE_CLASS;
	extern std::map<int, std::string> OS_ABI;
	extern std::map<int, std::string> MACHINE_ARCHITECTURES;

	extern std::map<int, std::string> PROGRAM_TYPE;
	extern std::map<int, std::string> PROGRAM_FLAG;

	extern std::map<int, std::string> SECTION_TYPE;


#ifdef __cplusplus
}
#endif

#endif // __ELFFORMAT_H__
