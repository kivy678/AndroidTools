console.log("[*] Start Script");

var libc = Module.load('libc.so');
var read_addr = null;

libc.enumerateExports().forEach(function(element) {
    //console.log(element.name);
    if (element.name == 'read') {
        console.log("[*] read: ", element.address);
        read_addr = element.address;
    };
});

console.log(hexdump(read_addr, { length: 16, ansi: true }));


Interceptor.attach(Module.getExportByName('libc.so', 'read'), {
  onEnter: function (args) {

    // void *mmap(void *addr, size_t length, int prot, int flags, int fd, off_t offset);
    // char* fgets(char* str, int num, FILE* stream);
    // void *dlsym(void *handle, const char *symbol);
    // ssize_t read (int fd, void *buf, size_t nbytes);
      console.log("#############################");
    console.log(hexdump(read_addr, { length: 16, ansi: true }));
    console.log("#############################");

  }
  /*
  ,onLeave: function (result) {
  }
  */
})


console.log("[*] End Script");
