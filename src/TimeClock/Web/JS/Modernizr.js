/*! modernizr 3.3.1 (Custom Build) | MIT *
 * http://modernizr.com/download/?-cookies-input-inputtypes-setclasses !*/
!function(e,t,n){function a(e,t){return typeof e===t}function i(){var e,t,n,i,o,s,c;for(var u in r)if(r.hasOwnProperty(u)){if(e=[],t=r[u],t.name&&(e.push(t.name.toLowerCase()),t.options&&t.options.aliases&&t.options.aliases.length))for(n=0;n<t.options.aliases.length;n++)e.push(t.options.aliases[n].toLowerCase());for(i=a(t.fn,"function")?t.fn():t.fn,o=0;o<e.length;o++)s=e[o],c=s.split("."),1===c.length?Modernizr[c[0]]=i:(!Modernizr[c[0]]||Modernizr[c[0]]instanceof Boolean||(Modernizr[c[0]]=new Boolean(Modernizr[c[0]])),Modernizr[c[0]][c[1]]=i),l.push((i?"":"no-")+c.join("-"))}}function o(e){var t=u.className,n=Modernizr._config.classPrefix||"";if(f&&(t=t.baseVal),Modernizr._config.enableJSClass){var a=new RegExp("(^|\\s)"+n+"no-js(\\s|$)");t=t.replace(a,"$1"+n+"js$2")}Modernizr._config.enableClasses&&(t+=" "+n+e.join(" "+n),f?u.className.baseVal=t:u.className=t)}function s(){return"function"!=typeof t.createElement?t.createElement(arguments[0]):f?t.createElementNS.call(t,"http://www.w3.org/2000/svg",arguments[0]):t.createElement.apply(t,arguments)}var l=[],r=[],c={_version:"3.3.1",_config:{classPrefix:"",enableClasses:!0,enableJSClass:!0,usePrefixes:!0},_q:[],on:function(e,t){var n=this;setTimeout(function(){t(n[e])},0)},addTest:function(e,t,n){r.push({name:e,fn:t,options:n})},addAsyncTest:function(e){r.push({name:null,fn:e})}},Modernizr=function(){};Modernizr.prototype=c,Modernizr=new Modernizr,Modernizr.addTest("cookies",function(){try{t.cookie="cookietest=1";var e=-1!=t.cookie.indexOf("cookietest=");return t.cookie="cookietest=1; expires=Thu, 01-Jan-1970 00:00:01 GMT",e}catch(n){return!1}});var u=t.documentElement,f="svg"===u.nodeName.toLowerCase(),p=s("input"),d="autocomplete autofocus list placeholder max min multiple pattern required step".split(" "),m={};Modernizr.input=function(t){for(var n=0,a=t.length;a>n;n++)m[t[n]]=!!(t[n]in p);return m.list&&(m.list=!(!s("datalist")||!e.HTMLDataListElement)),m}(d);var h="search tel url email datetime date month week time datetime-local number range color".split(" "),g={};Modernizr.inputtypes=function(e){for(var a,i,o,s=e.length,l="1)",r=0;s>r;r++)p.setAttribute("type",a=e[r]),o="text"!==p.type&&"style"in p,o&&(p.value=l,p.style.cssText="position:absolute;visibility:hidden;",/^range$/.test(a)&&p.style.WebkitAppearance!==n?(u.appendChild(p),i=t.defaultView,o=i.getComputedStyle&&"textfield"!==i.getComputedStyle(p,null).WebkitAppearance&&0!==p.offsetHeight,u.removeChild(p)):/^(search|tel)$/.test(a)||(o=/^(url|email)$/.test(a)?p.checkValidity&&p.checkValidity()===!1:p.value!=l)),g[e[r]]=!!o;return g}(h),i(),o(l),delete c.addTest,delete c.addAsyncTest;for(var v=0;v<Modernizr._q.length;v++)Modernizr._q[v]();e.Modernizr=Modernizr}(window,document);