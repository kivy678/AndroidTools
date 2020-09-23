CC=my-toolchain-22/bin/i686-linux-android-clang
ELF_CLEANER=./cleaner_x64

OBJS=GetMemory.o ReadMemory.o SearchMemory.o WriteMemory.o
TARGET=GetMemory_x86 ReadMemory_x86 SearchMemory_x86 WriteMemory_x86

all: $(TARGET)

$(TARGET): $(OBJS)
	$(CC) -o $@ $<
	$(ELF_CLEANER) $@

clean:
	rm -f $(OBJS) $(TARGET)
	