console.log("[*] Start Script");

Java.perform(function () {
	
  console.log("[*] start Hook");
  try {

    
  	//ssize_t read(int fd, void *buf, size_t count);
Interceptor.attach(Module.getExportByName(null, 'read'), {
  onEnter: function (args) {
    console.log('Context  : ' + JSON.stringify(this.context));
    console.log('ReturnAddr : ' + this.returnAddress);

    this.fd     = args[0].toInt32();
    this.buf    = args[1];
    this.count  = args[2].toInt32();
  },
  onLeave: function (result) {
    var numBytes = result.toInt32();
    if (numBytes > 0) {
      console.log(hexdump(this.buf, { length: numBytes, ansi: true }));
    }
    console.log('Result   : ' + numBytes);
  }
})



  } catch (e) {
  	console.log(e.name, e.message);
  }


  console.log("[*] end Hook");

});

console.log("[*] End Script");
