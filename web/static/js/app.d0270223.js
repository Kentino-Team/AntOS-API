(function(t){function e(e){for(var r,o,u=e[0],i=e[1],s=e[2],l=0,b=[];l<u.length;l++)o=u[l],Object.prototype.hasOwnProperty.call(c,o)&&c[o]&&b.push(c[o][0]),c[o]=0;for(r in i)Object.prototype.hasOwnProperty.call(i,r)&&(t[r]=i[r]);f&&f(e);while(b.length)b.shift()();return a.push.apply(a,s||[]),n()}function n(){for(var t,e=0;e<a.length;e++){for(var n=a[e],r=!0,u=1;u<n.length;u++){var i=n[u];0!==c[i]&&(r=!1)}r&&(a.splice(e--,1),t=o(o.s=n[0]))}return t}var r={},c={app:0},a=[];function o(e){if(r[e])return r[e].exports;var n=r[e]={i:e,l:!1,exports:{}};return t[e].call(n.exports,n,n.exports,o),n.l=!0,n.exports}o.m=t,o.c=r,o.d=function(t,e,n){o.o(t,e)||Object.defineProperty(t,e,{enumerable:!0,get:n})},o.r=function(t){"undefined"!==typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(t,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(t,"__esModule",{value:!0})},o.t=function(t,e){if(1&e&&(t=o(t)),8&e)return t;if(4&e&&"object"===typeof t&&t&&t.__esModule)return t;var n=Object.create(null);if(o.r(n),Object.defineProperty(n,"default",{enumerable:!0,value:t}),2&e&&"string"!=typeof t)for(var r in t)o.d(n,r,function(e){return t[e]}.bind(null,r));return n},o.n=function(t){var e=t&&t.__esModule?function(){return t["default"]}:function(){return t};return o.d(e,"a",e),e},o.o=function(t,e){return Object.prototype.hasOwnProperty.call(t,e)},o.p="/";var u=window["webpackJsonp"]=window["webpackJsonp"]||[],i=u.push.bind(u);u.push=e,u=u.slice();for(var s=0;s<u.length;s++)e(u[s]);var f=i;a.push([0,"chunk-vendors"]),n()})({0:function(t,e,n){t.exports=n("56d7")},"29fd":function(t,e,n){"use strict";n("3195")},3195:function(t,e,n){},"56d7":function(t,e,n){"use strict";n.r(e);n("e260"),n("e6cf"),n("cca6"),n("a79d");var r=n("7a23");function c(t,e,n,c,a,o){var u=Object(r["R"])("router-view");return Object(r["I"])(),Object(r["k"])(u)}var a={name:"App"},o=(n("dcca"),n("6b0d")),u=n.n(o);const i=u()(a,[["render",c]]);var s=i,f=n("6c02"),l=(n("b0c0"),{class:"home"});function b(t,e,n,c,a,o){var u=this,i=Object(r["R"])("FarmCard"),s=Object(r["R"])("el-col"),f=Object(r["R"])("el-row");return Object(r["I"])(),Object(r["m"])("div",l,[Object(r["q"])(f,{gutter:16},{default:Object(r["gb"])((function(){return[(Object(r["I"])(!0),Object(r["m"])(r["b"],null,Object(r["P"])(a.farms,(function(t){return Object(r["I"])(),Object(r["k"])(s,{key:t,span:8,xs:24,class:"el-farm-col"},{default:Object(r["gb"])((function(){return[Object(r["q"])(i,{title:t.name,onClick:function(){return u.farm_click(t["_id"]["$oid"])},workers:t.workers},null,8,["title","onClick","workers"])]})),_:2},1024)})),128))]})),_:1})])}var d=n("1da1"),p=(n("96cf"),n("bc3a")),O=n.n(p),j={get_farms:function(){var t=Object(d["a"])(regeneratorRuntime.mark((function t(){return regeneratorRuntime.wrap((function(t){while(1)switch(t.prev=t.next){case 0:return t.next=2,O.a.get("http://localhost:80/farm");case 2:return t.abrupt("return",t.sent);case 3:case"end":return t.stop()}}),t)})));function e(){return t.apply(this,arguments)}return e}(),get_farm:function(){var t=Object(d["a"])(regeneratorRuntime.mark((function t(e){return regeneratorRuntime.wrap((function(t){while(1)switch(t.prev=t.next){case 0:return t.next=2,O.a.get("http://localhost:80/farm/"+e);case 2:return t.abrupt("return",t.sent);case 3:case"end":return t.stop()}}),t)})));function e(e){return t.apply(this,arguments)}return e}()},m=j,h=function(t){return Object(r["L"])("data-v-82a116fa"),t=t(),Object(r["J"])(),t},v={class:"farm-card"},g={class:"card-header"},_={class:"card-title"},w=h((function(){return Object(r["n"])("span",{class:"mdi mdi-flash"},null,-1)})),k=h((function(){return Object(r["n"])("span",{class:"mdi mdi-pickaxe"},null,-1)}));function y(t,e,n,c,a,o){var u=Object(r["R"])("el-tag"),i=Object(r["R"])("el-col"),s=Object(r["R"])("el-row"),f=Object(r["R"])("el-card");return Object(r["I"])(),Object(r["m"])("div",v,[Object(r["q"])(f,{class:Object(r["z"])("box-card-"+(o.is_online?"online":"offline")),shadow:"hover"},{header:Object(r["gb"])((function(){return[Object(r["n"])("div",g,[Object(r["n"])("span",_,Object(r["V"])(n.title),1),Object(r["q"])(u,{type:"info",class:"card-header-tag"},{default:Object(r["gb"])((function(){return[Object(r["p"])(Object(r["V"])(n.workers.length)+" worker"+Object(r["V"])(o.plurial_worker),1)]})),_:1})])]})),default:Object(r["gb"])((function(){return[Object(r["q"])(s,null,{default:Object(r["gb"])((function(){return[Object(r["q"])(i,{span:12},{default:Object(r["gb"])((function(){return[Object(r["n"])("span",null,[Object(r["p"])(Object(r["V"])(o.total_power)+"W ",1),w])]})),_:1}),Object(r["q"])(i,{span:12},{default:Object(r["gb"])((function(){return[Object(r["n"])("span",null,[Object(r["p"])(Object(r["V"])(o.total_khs)+"kh/s ",1),k])]})),_:1})]})),_:1})]})),_:1},8,["class"])])}n("d81d");var x={name:"FarmCard",props:{title:String,workers:Array},methods:{reducing_acc:function(t,e){return t+e}},computed:{plurial_worker:function(){return this.workers.length<=1?"":"s"},total_khs:function(){return this.workers.map((function(t){var e;return 0|(null===(e=t.stats)||void 0===e?void 0:e.total_khs)})).reduce(this.reducing_acc)},total_power:function(){var t=this;return this.workers.map((function(e){var n;return 0|(null===(n=e.stats)||void 0===n?void 0:n.power.reduce(t.reducing_acc))})).reduce(this.reducing_acc)},is_online:function(){return this.total_power>0}}};n("b894");const R=u()(x,[["render",y],["__scopeId","data-v-82a116fa"]]);var I=R,P={name:"Home",components:{FarmCard:I},data:function(){return{farms:[]}},mounted:function(){var t=this;m.get_farms().then((function(e){t.farms=e.data}))},methods:{farm_click:function(t){this.$router.push("/farm/"+t)}}};n("29fd");const q=u()(P,[["render",b],["__scopeId","data-v-b5e635ca"]]);var S=q,V={class:"farm"};function C(t,e,n,c,a,o){return Object(r["I"])(),Object(r["m"])("div",V,[Object(r["n"])("h1",null,Object(r["V"])(a.farm.name),1)])}var F={name:"Farm",data:function(){return{farm:{}}},mounted:function(){var t=this;m.get_farm(this.$route.params.id).then((function(e){t.farm=e.data}))}};const M=u()(F,[["render",C]]);var J=M,$=[{path:"/",name:"Home",component:S},{path:"/farm/:id",name:"Farm",component:J}],A=Object(f["a"])({history:Object(f["b"])(),routes:$}),H=A,T=n("5502"),z=Object(T["a"])({state:{},mutations:{},actions:{},modules:{}}),L=n("7864"),W=(n("7dd6"),function(t){t.use(L["a"])}),B=(n("41e6"),Object(r["j"])(s));W(B),B.use(z).use(H).mount("#app")},b894:function(t,e,n){"use strict";n("f12f")},dcca:function(t,e,n){"use strict";n("e647")},e647:function(t,e,n){},f12f:function(t,e,n){}});
//# sourceMappingURL=app.d0270223.js.map