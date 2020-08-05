
console.log("[*] Start Script");

Interceptor.attach(Module.getExportByName('libc.so', 'mmap'), {
  onEnter: function (args) {
    var enter = new Object();

    enter.context = JSON.stringify(this.context);
    enter.return = this.returnAddress;

    //void *mmap(void *addr, size_t length, int prot, int flags, int fd, off_t offset);
    enter.length = args[1].toInt32();
    send(enter)

  }/*,
  onLeave: function (result) {
    var leave = new Object();
    //var numBytes = result.toInt32();
    //if (numBytes > 0) {
    //  console.log(hexdump(this.buf, { length: numBytes, ansi: true }));
    //}
    leave.addr = result;
    send(leave)
  //}
  */
})

console.log("[*] End Script");
