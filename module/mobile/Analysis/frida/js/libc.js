
console.log("[*] Start Script");

Interceptor.attach(Module.getExportByName('libc.so', 'mmap'), {
  onEnter: function (args) {
    var context = new Object();
    context.context = JSON.stringify(this.context);
    context.return = this.returnAddress;

    send(context)


    //console.log('Context  : ' + JSON.stringify(this.context));
    //console.log('Return   : ' + this.returnAddress);
    //console.log('ThreadId : ' + this.threadId);
    //console.log('Depth    : ' + this.depth);
    //console.log('Errornr  : ' + this.err);

    //void *mmap(void *addr, size_t length, int prot, int flags, int fd, off_t offset);
    //this.length = args[1].toInt32();

    //console.log('length  : ' + this.length);

  }
  //onLeave: function (result) {
    // Show argument 1 (buf), saved during onEnter.
    //var numBytes = result.toInt32();
    //if (numBytes > 0) {
    //  console.log(hexdump(this.buf, { length: numBytes, ansi: true }));
    //}
    //console.log('addr   : ' + result);
  //}
  
})

console.log("[*] End Script");
