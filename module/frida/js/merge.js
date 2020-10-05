
//-- -----------------------------------------------------------------------------
//-- BEGIN libc-1-dlopen.js

// void *dlopen(const char *filename, int flag);
Interceptor.attach(Module.getExportByName(null, 'dlopen'), {
  onEnter: function (args) {
    //console.log('Context  : '   + JSON.stringify(this.context));
    //console.log('ReturnAddr : ' + this.returnAddress);

    this.filename     = args[0];
    this.flag         = args[1].toInt32();
  },
  onLeave: function (result) {
    var addr = result;

    send('dlopenName : ' + this.filename);
  }
})

//-- END libc-1-dlopen.js
//-- -----------------------------------------------------------------------------


//-- -----------------------------------------------------------------------------
//-- BEGIN libc-1-read.js

// ssize_t read(int fd, void *buf, size_t count);
Interceptor.attach(Module.getExportByName(null, 'read'), {
  onEnter: function (args) {
    //console.log('Context  : '   + JSON.stringify(this.context));
    //console.log('ReturnAddr : ' + this.returnAddress);

    this.fd     = args[0].toInt32();
    this.buf    = args[1];
    this.count  = args[2].toInt32();
  },
  onLeave: function (result) {
    var numBytes = result.toInt32();

    if (numBytes > 0) {
      send(hexdump(this.buf, { length: numBytes, ansi: false }));
    }

    send('ReadCount   : ' + numBytes);
  }
})

//-- END libc-1-read.js
//-- -----------------------------------------------------------------------------


//-- -----------------------------------------------------------------------------
//-- BEGIN libc-1-write.js

// ssize_t write(int fd, const void *buf, size_t count);
Interceptor.attach(Module.getExportByName(null, 'write'), {
  onEnter: function (args) {
    //console.log('Context  : '   + JSON.stringify(this.context));
    //console.log('ReturnAddr : ' + this.returnAddress);

    this.fd     = args[0].toInt32();
    this.buf    = args[1];
    this.count  = args[2].toInt32();
  },
  onLeave: function (result) {
    var numBytes = result.toInt32();

    if (numBytes > 0) {
      send(hexdump(this.buf, { length: numBytes, ansi: false }));
    }

    send('WriteCount   : ' + numBytes);
  }
})

//-- END libc-1-write.js
//-- -----------------------------------------------------------------------------

