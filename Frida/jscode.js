
console.log("[*] Start Script");

Java.perform(function() {
	
    console.log("[*] start Hook");

    var libc = Module.findBaseAddress('libfoo.so');

    console.log(hexdump(libc, {
    	offset: 0,
    	length: 128,
    	header: true,
    	ansi: true

    }));



    console.log("[*] end Hook");
});


console.log("[*] End Script");

