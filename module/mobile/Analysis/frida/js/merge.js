
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
//-- BEGIN libc-1-dlsym.js

// void *dlsym(void *handle, const char *symbol);
Interceptor.attach(Module.getExportByName(null, 'dlsym'), {
  onEnter: function (args) {
    //console.log('Context  : '   + JSON.stringify(this.context));
    //console.log('ReturnAddr : ' + this.returnAddress);

    this.handle     = args[0];
    this.symbol     = args[1];
  },
  onLeave: function (result) {
    var addr = result;

    send('dlsymName : ' + this.symbol);
    send('dlsymAddr : ' + addr);
  }
})

//-- END libc-1-dlsym.js
//-- -----------------------------------------------------------------------------


//-- -----------------------------------------------------------------------------
//-- BEGIN libc-1-fgets.js

// char* fgets(char* str, int num, FILE* stream);
Interceptor.attach(Module.getExportByName(null, 'fgets'), {
  onEnter: function (args) {
    //console.log('Context  : '   + JSON.stringify(this.context));
    //console.log('ReturnAddr : ' + this.returnAddress);

    this.str     = args[0];
    this.num     = args[1].toInt32();
    this.stream  = args[2];
  },
  onLeave: function (result) {
    console.log("fets: ");
    if (this.num > 0) {
      send(hexdump(this.str, { length: this.num, ansi: true }));
    }
  }
})

//-- END libc-1-fgets.js
//-- -----------------------------------------------------------------------------


//-- -----------------------------------------------------------------------------
//-- BEGIN libc-1-mmap.js

// void *mmap(void *addr, size_t length, int prot, int flags, int fd, off_t offset);
Interceptor.attach(Module.getExportByName(null, 'mmap'), {
  onEnter: function (args) {
    //console.log('Context  : '   + JSON.stringify(this.context));
    //console.log('ReturnAddr : ' + this.returnAddress);

    this.addr     = args[0];
    this.length   = args[1].toInt32();
    this.prot     = args[2].toInt32();
    this.flags    = args[3].toInt32();
    this.fd       = args[4].toInt32();
    this.offset   = args[5].toInt32();
  },
  onLeave: function (result) {
    var addr = result;

    send('mmapAddr   : ' + addr);
    send('mmaplength : ' + this.length);
  }
})

//-- END libc-1-mmap.js
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
      send(hexdump(this.buf, { length: numBytes, ansi: true }));
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
      send(hexdump(this.buf, { length: numBytes, ansi: true }));
    }

    send('WriteCount   : ' + numBytes);
  }
})

//-- END libc-1-write.js
//-- -----------------------------------------------------------------------------

