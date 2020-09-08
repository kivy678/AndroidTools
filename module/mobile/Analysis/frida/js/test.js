
console.log("[*] Start Script");

Java.perform(function () {
	
  console.log("[*] start Hook");
  try {
  	var linker_addr = null;
  	var linker_size = null;

    Process.enumerateModules().forEach(function(element) {
        //if (element.name == 'libil2cpp.so') {
            console.log("[*] Module Name: ", element.name);
            linker_addr = element.base;				// native pointer
            linker_size = element.size;
        //};
	 })


  linker_addr = Process.enumerateModules('libc.so');
  console.log(linker_addr);



  } catch (e) {
  	console.log(e.name, e.message);
  }


    console.log("[*] end Hook");

});

console.log("[*] End Script");
