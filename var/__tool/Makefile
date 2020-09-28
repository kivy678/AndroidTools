CC=my-toolchain-22/bin/clang
ELF_CLEANER=./cleaner_x64

TARGET=GetMemory ReadMemory SearchMemory WriteMemory

all: $(TARGET)

$(TARGET): %: %.c
	$(CC) -o $@ $<
	$(ELF_CLEANER) $@

clean:
	rm -rf $(TARGET)
	