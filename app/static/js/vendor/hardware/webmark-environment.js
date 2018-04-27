let uaparser = new UAParser();
let uaresult = uaparser.getResult();
let canvas, gl, glVender, glRenderer, debugInfo;

function getCanvas() {
  if (canvas == null) {
    canvas = document.createElement('canvas');
  }
  return canvas;
}

function getGl() {
  if (gl == null) {
    gl = getCanvas().getContext('experimental-webgl');
  }
  return gl;
}

function getGlVender() {
  if (glVender == null) {
    debugInfo = getGl().getExtension('WEBGL_debug_renderer_info');
    //Return the VENDOR string of the underlying graphics driver
    glVender = debugInfo == null ? 'unknown' : getGl().getParameter(debugInfo.UNMASKED_VENDOR_WEBGL);
  }
  return glVender;
}

function getGlRenderer() {
  if (glRenderer == null) {
    debugInfo = getGl().getExtension('WEBGL_debug_renderer_info');
    //Return the RENDERER string of the underlying graphics driver
    glRenderer = debugInfo == null ? 'unknown' : getGl().getParameter(debugInfo.UNMASKED_RENDERER_WEBGL);
  }
  return glRenderer;
}

function getScreenWidth() {
  return screen.width * (window.devicePixelRatio || 1);
}

function getScreenHeight() {
  return screen.height * (window.devicePixelRatio || 1);
}

// Return the number of logical processors available to run threads on the user's computer
function getHardwareConcurrency() {
  if (navigator.hardwareConcurrency) {
    return navigator.hardwareConcurrency;
  }
  return undefined;
}

// Return the amount of device memory in gigabytes. 
// This value is an approximation given by rounding to the nearest power of 2 
// and dividing that number by 1024.
// Device-Memory Client Hint header and JS API will only be available to HTTPS secure contexts
function getDeviceMemory() {
  if (navigator.deviceMemory) {
    return navigator.deviceMemory;
  }
  return undefined;
}

function getTouchSupport() {
  let maxTouchPoints = 0;
  let touchEvent = false;
  if (typeof navigator.maxTouchPoints !== 'undefined') {
    maxTouchPoints = navigator.maxTouchPoints;
  } else if (typeof navigator.msMaxTouchPoints !== 'undefined') {
    maxTouchPoints = navigator.msMaxTouchPoints;
  }
  try {
    document.createEvent('TouchEvent');
    touchEvent = true;
  } catch (_) {};
  let touchStart = 'ontouchstart' in window;
  return [maxTouchPoints, touchEvent, touchStart];
}

function getTimezoneOffsetInHours() {
  let d = new Date();
  return (d.getTimezoneOffset() > 0 ? '-' : '+') + (d.getTimezoneOffset() / -60);
}

if(typeof(String.prototype.trim) === "undefined")
{
    String.prototype.trim = function()
    {
        return String(this).replace(/^\s+|\s+$/g, '');
    };
}

let WebMarkEnvironment = function () {
  this.hardware = () => {
      return {
        devicevendor: uaresult.device.vendor,
        devicemodel: uaresult.device.model,
        devicetype: uaresult.device.type,
        cpuarchitecture: uaresult.cpu.architecture,
        cpuhardwareconcurrency: getHardwareConcurrency(),
        gpuvender: getGlVender(),
        gpu: getGlRenderer(),
        devicememory: getDeviceMemory(),
        screenwidth: getScreenWidth(),
        screenheight: getScreenHeight(),
        screenavailablewidth: screen.availWidth,
        screenavailableheight: screen.availHeight,
        screencolordepth: screen.colorDepth,
        screenpixeldepth: screen.pixelDepth,
        devicepixelratio: window.devicePixelRatio
      }
    },
    this.software = () => {
      return {
        os: uaresult.os.name,
        osversion: uaresult.os.version,
        platform: navigator.platform,
        timezone: getTimezoneOffsetInHours()
      }
    },
    this.browser = () => {
      return {
        name: uaresult.browser.name,
        version: uaresult.browser.version,
        major: uaresult.browser.major,
        language: navigator.language,
        enginename: uaresult.engine.name,
        engineversion: uaresult.engine.version,
        useragent: navigator.userAgent
      }
    },
    this.result = () => {
      return {
        hardware: {
          devicevendor: uaresult.device.vendor,
          devicemodel: uaresult.device.model,
          devicetype: uaresult.device.type,
          cpuarchitecture: uaresult.cpu.architecture,
          cpuhardwareconcurrency: getHardwareConcurrency(),
          gpuvender: getGlVender(),
          gpu: getGlRenderer().trim(),
          devicememory: getDeviceMemory(),
          screenwidth: getScreenWidth(),
          screenheight: getScreenHeight(),
          screenavailablewidth: screen.availWidth,
          screenavailableheight: screen.availHeight,
          screencolordepth: screen.colorDepth,
          screenpixeldepth: screen.pixelDepth,
          devicepixelratio: window.devicePixelRatio
        },
        software: {
          os: uaresult.os.name,
          osversion: uaresult.os.version,
          platform: navigator.platform,
          timezone: getTimezoneOffsetInHours()
        },
        browser: {
          name: uaresult.browser.name,
          version: uaresult.browser.version,
          major: uaresult.browser.major,
          language: navigator.language,
          enginename: uaresult.engine.name,
          engineversion: uaresult.engine.version,
          useragent: navigator.userAgent
        }
      }
    }
}

// let Hardware = function () {
//   this.devicevendor = () => {
//       return uaresult.device.vendor;
//     },
//     this.devicemodel = () => {
//       return uaresult.device.model;
//     },
//     this.devicetype = () => {
//       return uaresult.device.type;
//     },
//     this.cpuarchitecture = () => {
//       return uaresult.cpu.architecture;
//     },
//     this.gpuvender = () => {
//       return getGlVender();
//     },
//     this.gpu = () => {
//       return getGlRenderer();
//     },
//     this.result = () => {
//       return {
//         devicevendor: this.devicevendor(),
//         devicemodel: this.devicemodel(),
//         devicetype: this.devicetype(),
//         cpuarchitecture: this.cpuarchitecture(),
//         gpuvender: this.gpuvender(),
//         gpu: this.gpu()
//       }
//     }
// }

// let Software = function () {
//   this.os = () => {
//       return uaresult.os.name;
//     },
//     this.osversion = () => {
//       return uaresult.os.version;
//     },
//     this.result = () => {
//       return {
//         os: this.os(),
//         osversion: this.osversion()
//       }
//     }
// }

// let Browser = function () {
//   this.name = () => {
//       return uaresult.browser.name;
//     },
//     this.version = () => {
//       return uaresult.browser.version;
//     },
//     this.major = () => {
//       return uaresult.browser.major;
//     },
//     this.language = () => {
//       return navigator.language;
//     },
//     this.engineversion = () => {
//       return uaresult.engine.version;
//     },
//     this.engineversion = () => {
//       return uaresult.engine.version;
//     },
//     this.result = () => {
//       return {
//         name: this.name(),
//         version: this.version(),
//         major: this.major(),
//         language: this.language(),
//         enginename: this.enginename(),
//         engineversion: this.engineversion()
//       }
//     }
// }