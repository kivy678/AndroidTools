CC=my-toolchain-24/bin/i686-linux-android-clang
ELF_CLEANER=./cleaner_x64

TARGET=GetMemory ReadMemory SearchMemory WriteMemory

all: $(TARGET)

$(TARGET): %: %.c
	$(CC) -o $@ $<
	$(ELF_CLEANER) $@

clean:
	rm -rf $(TARGET)
	