import{BS as e,Gb as t,Jb as n,Jx as r,Kb as i,NI as a,OI as o,TI as s,VS as c,WS as l,Yx as u,bI as d,db as f,fB as p,hS as m,nF as h,qb as g,wI as _,yb as v}from"./app-core.js";import{M as y,N as b,P as x}from"./cds.js";var ee=[{kind:`info`,emoji:`ℹ️`,icon:b},{kind:`success`,emoji:`✅`,icon:x},{kind:`warning`,emoji:`⚠️`,icon:y}],te=/^(\u2139\uFE0F|\u2705\uFE0F?|\u26A0\uFE0F)( ?)/u,S=`[data-lfile-doc] .ProseMirror blockquote.ldoc-callout[data-callout]`,C=`${S}{position:relative;box-sizing:border-box;margin-top:.9em;margin-bottom:.9em;padding-block:10px;padding-inline:42px 40px;border:0;border-radius:var(--cds-radius--lg,10px);background:var(--cds-bg-accent,#cde2fb);color:var(--cds-text-primary,#0b0b0b)}${S}[data-callout=success]{background:var(--cds-bg-success,#caeac7)}${S}[data-callout=warning]{background:var(--cds-bg-warning,#f9dca4)}${S}>*{margin-inline-start:0}@media (max-width:480px) and (pointer:coarse){${(e=>`${S}>${e}{max-width:calc(100% + 28px)}${S}[${m}]>${e},[data-lfile-doc] .ProseMirror [${m}] blockquote.ldoc-callout[data-callout]:not([${m}])>${e}{max-width:100%}`)(`div[data-lfile-embed][data-lfile-embed-sized]`)}}${S}>p{margin-top:0;margin-bottom:0}${S}>p+p,${S}>p+.lfile-gap+p{margin-top:.4em}${S}>:first-child,${S}>.lfile-gap:first-child+*{text-indent:-28px}${S}>:is(p,h1,h2,h3,h4,h5,h6):first-child>*,${S}>.lfile-gap:first-child+:is(p,h1,h2,h3,h4,h5,h6)>*{text-indent:0}${S} .ldoc-callout-lead{display:inline-block;width:28px;text-indent:0;vertical-align:top;white-space:pre;color:transparent;caret-color:var(--cds-text-primary,#0b0b0b)}${S} .ldoc-callout-gap{display:inline-block;width:0;text-indent:0;vertical-align:top;white-space:pre;color:transparent;caret-color:var(--cds-text-primary,#0b0b0b)}${S}>.ldoc-callout-kind{position:absolute;inset-inline-start:10px;top:10px;width:26px;height:26px;margin:0;padding:0;text-indent:0;display:inline-flex;align-items:center;justify-content:center;border:0;border-radius:var(--cds-radius,6px);background:transparent;color:var(--cds-text-accent,#2c6bd6);font:inherit;-webkit-user-select:none;user-select:none}${S}[data-callout=success]>.ldoc-callout-kind{color:var(--cds-text-success,#3c7a36)}${S}[data-callout=warning]>.ldoc-callout-kind{color:var(--cds-text-warning,#a15c00)}${S}>button.ldoc-callout-kind{cursor:pointer}${S}>button.ldoc-callout-kind:hover,${S}>button.ldoc-callout-kind[aria-expanded=true]{background:var(--cds-fill-ghost-hover,rgba(0,0,0,.075))}${S}>button.ldoc-callout-kind:focus-visible,${S}>.ldoc-callout-x:focus-visible{outline:2px solid var(--cds-fill-accent,#2c84db);outline-offset:1px}${S}>.ldoc-callout-x{position:absolute;top:10px;inset-inline-end:8px;width:26px;height:26px;margin:0;padding:0;text-indent:0;display:none;align-items:center;justify-content:center;border:0;border-radius:var(--cds-radius,6px);background:transparent;color:var(--cds-text-secondary,#5e5d59);cursor:pointer}${S}>.ldoc-callout-x:hover{background:var(--cds-fill-ghost-hover,rgba(0,0,0,.075));color:var(--cds-text-primary,#0b0b0b)}.ProseMirror[contenteditable=true] blockquote.ldoc-callout[data-callout]:hover>.ldoc-callout-x,.ProseMirror[contenteditable=true] blockquote.ldoc-callout[data-callout].has-caret>.ldoc-callout-x,${S}>.ldoc-callout-x:focus-visible{display:inline-flex}.ldoc-callout-menu{position:fixed;z-index:2147483646;min-width:160px;padding:4px;background:var(--cds-surface-popover,#fff);border-radius:10px;box-shadow:0 0 0 1px var(--cds-border,rgba(0,0,0,.1)),var(--cds-shadow-popover,0 8px 24px rgba(0,0,0,.12));font-family:var(--cds-font-sans,ui-sans-serif),system-ui;font-size:var(--cds-font-size-body,14px);line-height:var(--cds-leading-body,20px);color:var(--cds-text-primary,#0b0b0b)}.ldoc-callout-menu .row{display:flex;align-items:center;gap:8px;height:var(--cds-h-control,28px);padding:0 10px;border-radius:var(--cds-radius,6px);cursor:pointer;outline:0}@media (pointer:coarse){.ldoc-callout-menu .row{height:40px}}.ldoc-callout-menu .row:hover,.ldoc-callout-menu .row:focus,.ldoc-callout-menu .row.is-sel{background:var(--cds-fill-ghost-hover,rgba(0,0,0,.075))}`+u(`.ldoc-callout-menu .row:focus`)+`.ldoc-callout-menu .row svg{flex:none;color:var(--cds-text-secondary,#5e5d59)}.ldoc-callout-menu .row[aria-selected=true] .tick{margin-left:auto;color:var(--cds-text-secondary,#5e5d59)}`,w=`ldoc-objmenu`,T=`ldoc-more`,E=`ldoc-objhost`,D=`data-objmenu`,O=`ldoc-objmenu-css`,k=`data-objmenu-seat`,A=(e,t)=>{let n=e.search(/[\s>+~]/);return`[${k}=inset] ${e}{${t}}${n<0?`${e}[${k}=inset]`:`${e.slice(0,n)}[${k}=inset]${e.slice(n)}`}{${t}}`},ne=`ldoc-tapped`,re=`border:0;background:var(--cds-surface-popover,#ffffff);border-radius:calc(var(--cds-radius,8px) + 4px);box-shadow:inset 0 0 0 var(--cds-ring-inner,0px) var(--cds-ring-color,rgba(11,11,11,.1)),0 0 0 var(--cds-ring-outer,1px) var(--cds-ring-color,rgba(11,11,11,.1)),var(--cds-shadow-popover,0 8px 24px rgba(0,0,0,.12),0 2px 6px rgba(0,0,0,.08))`,ie=`font-family:var(--cds-font-sans,var(--font-body,ui-sans-serif)),system-ui;font-size:var(--cds-font-size-body,14px);line-height:var(--cds-leading-body,20px);font-weight:400;color:var(--cds-text-primary,#0b0b0b)`,j=`var(--cds-fill-ghost-hover,rgba(11,11,11,.05))`,M=`box-shadow:var(--cds-focus-shadow,0 0 0 2px var(--cds-fill-accent,#2a78d6))`,ae=`outline:2px solid transparent;outline-offset:1px;${M}`,N=(e=>`${e}{position:fixed;z-index:55;box-sizing:border-box;display:flex;flex-direction:column;min-width:160px;max-width:min(320px,calc(100vw - 16px));max-height:calc(100vh - 16px - var(${h},0px));overflow-x:hidden;overflow-y:auto;padding:4px;${re};${ie};-webkit-user-select:none;user-select:none;animation:none;transform:none}${e}[hidden]{display:none}${e}:focus{outline:0}`)(`.${w}`)+(e=>`${e} button{box-sizing:border-box;display:flex;align-items:center;gap:var(--cds-gap-xs,8px);width:100%;min-height:var(--cds-h-control,32px);margin:0;padding:0 10px;border:0;border-radius:var(--cds-radius,8px);background:transparent;color:inherit;font:inherit;text-align:left;white-space:nowrap;cursor:var(--cds-cursor-interactive,pointer)}${e} button:is(:hover,:focus-visible){background:${j}}${e} button:focus{outline:0;box-shadow:none}`+u(`${e} button:focus-visible`)+`${e} button[aria-disabled=true]{opacity:var(--cds-opacity-disabled,.4);cursor:default}${e} button[aria-disabled=true]:hover:not(:focus-visible){background:transparent}${e} button[aria-disabled=true]:focus-visible{${M}}${e} [role=separator]{flex:none;height:1px;margin:4px 0;background:var(--cds-border,rgba(11,11,11,.1))}${e} .grp{display:block;padding:4px 10px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;font-size:var(--cds-font-size-footnote,13px);line-height:var(--cds-leading-footnote,17px);font-weight:var(--cds-font-weight-medium,500);color:var(--cds-text-muted,#898781)}${e} button>.lb{flex:0 1 auto;min-width:0;overflow:hidden;text-overflow:ellipsis;padding-block:2px;margin-block:-2px}${e} .gs{display:inline-block;flex:none;width:16px;height:1px}${e} button>svg{flex:none;display:block;color:var(--cds-text-secondary,#52514e)}${e} button>.ck{margin-left:auto;padding-left:12px;display:inline-flex;color:var(--cds-text-primary,#0b0b0b)}${e} button[aria-checked=false]>.ck{visibility:hidden}${e}.react{flex-direction:row;min-width:0;max-width:none;gap:4px}${e}.react button{width:24px;min-height:24px;height:24px;padding:0;justify-content:center;border-radius:var(--cds-radius,8px);font-size:16px;line-height:1}${e}.react button>.lb{overflow:visible;text-overflow:clip}`+a(e)+`${e} button.danger[aria-disabled=true]:hover:not(:focus-visible){background:transparent;color:var(--cds-text-danger,#8e2626)}@media (pointer:coarse){${e} button{min-height:40px}${e}.react button{width:40px;height:40px;font-size:20px}}`)(`.${w}`)+(e=>`${e}{--more-size:28px;box-sizing:border-box;display:inline-flex;align-items:center;justify-content:center;flex:none;width:var(--more-size);height:var(--more-size);margin:0;padding:0;border:1px solid var(--cds-border,rgba(11,11,11,.1));border-radius:var(--cds-radius,8px);background:var(--cds-surface-3,#ffffff);color:var(--cds-text-secondary,#52514e);font:inherit;line-height:0;cursor:var(--cds-cursor-interactive,pointer);-webkit-user-select:none;user-select:none}${e}[hidden]{display:none}${e}>svg{display:block;width:14px;height:14px;pointer-events:none}${r(`${e}>svg`)}{width:20px;height:20px}${e}:is(:hover,[aria-expanded=true]){background-image:linear-gradient(${j},${j});color:var(--cds-text-primary,#0b0b0b)}${e}:focus{outline:0}${e}:focus-visible{${ae}}@media (pointer:coarse){${e}{--more-size:40px}${e}>svg{width:16px;height:16px}}`)(`button.${T}`)+((e,t)=>`:where(${e}){position:relative}${e}>${t}{display:none;position:absolute;z-index:3;top:var(--objmenu-top,0px);right:calc(0px - 8px - var(--more-size))}${e}>${t}::before{content:"";position:absolute;top:-4px;bottom:-4px;right:-4px;left:calc(0px - 8px)}`+A(`${e}>${t}`,`top:var(--objmenu-inset-top,6px);right:var(--objmenu-inset-right,6px)`)+A(`${e}>${t}::before`,`left:-4px`)+`${e}[${D}]:is(:focus-within,.has-caret,.cw-has-caret,.ProseMirror-selectednode,.${ne})>${t}:not([hidden]),${e}[${D}]>${t}:is([aria-expanded=true],:focus-visible):not([hidden]){display:inline-flex}@media (hover:hover){${e}[${D}]:hover>${t}:not([hidden]){display:inline-flex}}`)(`.${E}`,`button.${T}`),P=`cw-pane-sel`,F=1.5,I=`button[data-cds="Button"]`,L=`:is(:hover,:focus-within,.cw-has-caret,.ProseMirror-selectednode)`,R=`.lfile-codewrap:not(.cw-src-open):is([data-live="mermaid"],[data-live="latex"]) .cw-render.cw-mm-loading.cw-wait-box`,z=22,B=6,V=7,H=3,U=1,W=`
.lfile-codewrap{position:relative}
.lfile-codewrap.cw-renderable{background:#f8f8f6;border-radius:6px;margin:.6em 0}
[data-mode=dark] .lfile-codewrap.cw-renderable{background:var(--cds-surface-1)}
.lfile-codewrap.cw-renderable[data-live="mermaid"]:not(.cw-src-open){background:transparent}
.lfile-codewrap.cw-renderable pre{background:none;margin:0}
.lfile-codewrap .cw-head{position:absolute;top:${B}px;right:6px;z-index:2;display:inline-flex;gap:4px;align-items:center}
.lfile-codewrap.cw-renderable{padding-top:24px}
.lfile-codewrap.cw-renderable .cw-head{top:0;right:8px;height:24px}
.lfile-codewrap .cw-lang{display:inline-flex;align-items:center;height:${z}px;box-sizing:border-box;font-size:var(--cds-font-size-caption,11px);color:var(--cds-text-muted,#6f6b60);background:var(--cds-surface-1,#fff);border:1px solid var(--cds-border,#d8d5cc);border-radius:var(--cds-radius,6px);padding:0 8px;margin:0;font-family:inherit;line-height:inherit;cursor:pointer;user-select:none}
.lfile-codewrap .cw-lang[aria-disabled=true]{cursor:default}
@media (hover:hover){.lfile-codewrap.cw-src-open .cw-lang:not(.cw-lang-icon):not([aria-disabled=true]):hover{color:inherit;background:var(--cds-surface-2,#f2f0ea)}}
.lfile-codewrap .cw-lang.cw-lang-icon{border:0;background:none;padding:0 2px;cursor:default}
.lfile-codewrap .cw-srchead{position:relative;height:0;display:none}
.lfile-codewrap.cw-renderable.cw-src-open .cw-srchead{display:block}
.lfile-codewrap .cw-pick{position:absolute;top:${V}px;right:${V}px;z-index:2;display:inline-flex;gap:4px;align-items:center}
.lfile-codewrap .cw-langicon{flex:none;width:14px;height:14px;pointer-events:none}
${r(`.lfile-codewrap .cw-langicon`)}{width:20px;height:20px}
@media screen{.lfile-codewrap:not(.cw-renderable)>pre{padding-top:34px}}
@media screen and (pointer:coarse){${A(`.lfile-codewrap:not(.cw-renderable)>pre`,`padding-top:${2*H+40}px`)}}
[data-mode=dark] .lfile-codewrap{color-scheme:dark}
.lfile-codewrap .cw-render{text-align:center;padding:12px 8px;overflow-x:auto;user-select:none;-webkit-user-select:none;cursor:default}
.lfile-codewrap{--cw-sel:rgba(74,124,209,.30);--cw-hl:${v(15)};--cw-hl-on:${v(65)};--cw-hl-res:${n(18)};--cw-hl-res-on:${n(32)}}
html.cw-blur .lfile-codewrap{--cw-sel:rgba(140,140,140,.28)}
.lfile-codewrap ::highlight(bongo-live-src-hover){background-color:${v(40)}}
.lfile-codewrap ::highlight(bongo-live-sel){background-color:rgba(74,124,209,.30)}
html.cw-blur .lfile-codewrap ::highlight(bongo-live-sel){background-color:rgba(140,140,140,.28)}
.lfile-codewrap ::highlight(bongo-live-hl){background-color:${v(15)}}
.lfile-codewrap ::highlight(bongo-live-hl-on){background-color:${v(65)}}
.lfile-codewrap ::highlight(bongo-live-hl-res){background-color:${n(18)}}
.lfile-codewrap ::highlight(bongo-live-hl-res-on){background-color:${n(32)}}
.lfile-codewrap .cw-lx-sel{background:var(--cw-sel);border-radius:2px}
.lfile-codewrap .cw-lx-hl{background:var(--cw-hl);border-radius:2px;cursor:pointer}
.lfile-codewrap .cw-lx-hl.cw-on{background:var(--cw-hl-on)}
.lfile-codewrap .cw-lx-hl.cw-res{background:var(--cw-hl-res)}
.lfile-codewrap .cw-lx-hl.cw-res.cw-on{background:var(--cw-hl-res-on)}
.lfile-codewrap .cw-render .katex-display{margin:0}
.lfile-codewrap[data-live="markdown"] .cw-render{text-align:left;padding:14px 18px}
.lfile-codewrap[data-live="markdown"] .cw-render :is(h1,h2,h3,h4,h5,h6){margin:.5em 0 .25em;line-height:1.25}
.lfile-codewrap[data-live="markdown"] .cw-render h1{font-size:1.3em}
.lfile-codewrap[data-live="markdown"] .cw-render h2{font-size:1.18em}
.lfile-codewrap[data-live="markdown"] .cw-render :is(h3,h4){font-size:1.05em}
.lfile-codewrap[data-live="markdown"] .cw-render :is(h5,h6){font-size:1em}
.lfile-codewrap[data-live="markdown"] .cw-render p{margin:.25em 0}
.lfile-codewrap[data-live="csv"] .cw-render{text-align:left;padding:10px 14px;}
.lfile-codewrap:is([data-live="csv"],[data-live="markdown"]) table{width:100%;border-collapse:collapse;font-size:var(--cds-font-size-footnote,13px)}
.lfile-codewrap:is([data-live="csv"],[data-live="markdown"]) :is(th,td){border:1px solid var(--cds-border-strong,#c9c7c0);padding:3px 10px;text-align:left}
.lfile-codewrap:is([data-live="csv"],[data-live="markdown"]) th{font-weight:600;background:rgba(0,0,0,.04)}
.lfile-codewrap[data-live="csv"] :is(th,td).cw-csv-sel{background:var(--cw-sel)}
.lfile-codewrap[data-live="csv"] :is(th,td).cw-csv-hl{background:var(--cw-hl);cursor:pointer}
.lfile-codewrap[data-live="csv"] :is(th,td).cw-csv-hl.cw-on{background:var(--cw-hl-on)}
.lfile-codewrap[data-live="csv"] :is(th,td).cw-csv-hl.cw-res{background:var(--cw-hl-res)}
.lfile-codewrap[data-live="csv"] :is(th,td).cw-csv-hl.cw-res.cw-on{background:var(--cw-hl-res-on)}
[data-mode=dark] .lfile-codewrap:is([data-live="csv"],[data-live="markdown"]) th{background:rgba(255,255,255,.06)}
.lfile-codewrap[data-live="markdown"] .cw-render blockquote{margin:.25em 0;padding-left:10px;border-left:3px solid var(--cds-border-strong,#b8b6af)}
.lfile-codewrap[data-live="mermaid"] .cw-render{padding:14px 12px}
.lfile-codewrap[data-live="mermaid"] .cw-render svg{max-width:100%;height:auto}
.lfile-codewrap:is([data-live="mermaid"],[data-live="latex"]) .cw-render.cw-mm-loading{color:var(--cds-text-secondary,#6b6a65);font-size:var(--cds-font-size-footnote,12px)}
${e}
${l(R,`display:flex;align-items:center;justify-content:center;min-height:160px;margin:6px 0 8px;padding:0;overflow:hidden;pointer-events:auto`)}
.lfile-codewrap:not(.cw-src-open)[data-live="latex"] .cw-render.cw-mm-loading.cw-wait-box{min-height:56px}
.lfile-codewrap.cw-renderable[data-live="latex"]:not(.cw-src-open):has(.cw-render.cw-wait-box){background:transparent}
.lfile-codewrap:not(.cw-src-open):has(.cw-render.cw-wait-box) :is(.cw-lead,.cw-head){opacity:0;pointer-events:none;animation:cw-head-late 200ms linear ${c}ms forwards}
.lfile-codewrap:not(.cw-src-open):has(.cw-render.cw-wait-box):focus-within :is(.cw-lead,.cw-head){opacity:1;pointer-events:auto;animation:none}
@keyframes cw-head-late{to{opacity:1;pointer-events:auto}}
@media (prefers-reduced-motion:reduce){.lfile-codewrap:not(.cw-src-open):has(.cw-render.cw-wait-box) :is(.cw-lead,.cw-head){animation-duration:1ms}}
.lfile-codewrap[data-live="markdown"] .cw-md-task input[type=checkbox]{margin-right:6px;vertical-align:baseline}
.lfile-codewrap[data-live="mermaid"] .cw-mm-sel .cw-mm-txt-sel{background:var(--cw-sel);border-radius:2px}
.lfile-codewrap[data-live="mermaid"]:not(.cw-src-open) .cw-render{cursor:default}
.lfile-codewrap[data-live="mermaid"]:not(.cw-src-open) .cw-render :is(g.node,g.edgeLabel,g.cluster-label,g[name],rect[name],g.actor-man,.cw-mm-person-tile,rect.note){cursor:pointer}
.lfile-codewrap[data-live="mermaid"]:not(.cw-src-open) .cw-render :is(foreignObject *,text,tspan){user-select:text;-webkit-user-select:text;cursor:text}
.lfile-codewrap[data-live="markdown"]:not(.cw-src-open) .cw-render{cursor:text}
.lfile-codewrap[data-live="markdown"]:not(.cw-src-open).${P} .cw-render{user-select:text;-webkit-user-select:text}
.ProseMirror-hideselection .lfile-codewrap.${P} .cw-render ::selection{background-color:var(--cds-bg-accent,#cde2fb);color:var(--cds-text-accent,#184f95)}
[data-mode=dark] .ProseMirror-hideselection .lfile-codewrap.${P} .cw-render ::selection{background-color:var(--cds-bg-accent,#032042);color:var(--cds-text-accent,#6da7ec)}
.lfile-codewrap[data-live="mermaid"] .cw-mm-inplace:not(.cw-mm-part-sel)>:is(rect,circle,ellipse,polygon,path,line):not(.cw-mm-selbg,.cw-mm-hlbg),.lfile-codewrap[data-live="mermaid"] .cw-mm-inplace:not(.cw-mm-part-sel)>.cw-mm-person>.cw-mm-person-tile{stroke:var(--cds-fill-accent,#2a78d6)!important;stroke-width:2px!important}
.lfile-codewrap[data-live="mermaid"] svg text.cw-mm-inplace .cw-mm-txt-sel,.lfile-codewrap[data-live="mermaid"] svg .cw-mm-inplace text .cw-mm-txt-sel,.lfile-codewrap[data-live="mermaid"] svg .cw-mm-sel text .cw-mm-txt-sel,.lfile-codewrap[data-live="mermaid"] svg text.cw-mm-sel .cw-mm-txt-sel{text-decoration:none}
.lfile-codewrap[data-live="mermaid"] svg .cw-mm-selbg{fill:var(--cw-sel);stroke:none;pointer-events:none}
.lfile-codewrap[data-live="mermaid"] svg .cw-mm-hlbg{fill:${g.rest};stroke:none;pointer-events:none}
.lfile-codewrap[data-live="mermaid"] svg .cw-mm-hlbg.cw-on{fill:${g.on}}
.lfile-codewrap[data-live="mermaid"] svg .cw-mm-hlbg.cw-res{fill:${g.res}}
.lfile-codewrap[data-live="mermaid"] svg .cw-mm-hlbg.cw-res.cw-on{fill:${g.resOn}}
.lfile-codewrap .cw-mm-edit-host{position:absolute;inset:0;pointer-events:none;z-index:4}
.lfile-codewrap .cw-mm-edit{pointer-events:auto;position:absolute;z-index:4;transform:translate(-50%,-50%);box-sizing:border-box;margin:0;padding:0 2px;min-height:1em;border:0;border-width:0;border-style:none;border-radius:0;outline:0;outline-style:none;outline-width:0;box-shadow:none;background:transparent;background-color:transparent;color:var(--cds-text-primary,#141413);caret-color:auto;white-space:pre;text-align:center;cursor:text;user-select:text;-webkit-user-select:text}
.lfile-codewrap .cw-mm-edit:focus,.lfile-codewrap .cw-mm-edit:focus-visible{outline:0;outline-style:none;outline-width:0;box-shadow:none}
.lfile-codewrap .cw-mm-edit::selection{background:var(--cw-sel)}
.lfile-codewrap .cw-mm-edit-hint{position:absolute;z-index:4;transform:translateX(-50%);pointer-events:none;white-space:nowrap;font-size:11px;line-height:1.3;color:var(--cds-text-secondary,#6b6a65);background:var(--cds-surface-1,#fff);border:1px solid var(--cds-border,#d8d5cc);border-radius:4px;padding:2px 6px}
.lfile-codewrap.cw-mm-editing .cw-mm-inplace .cw-mm-txt-sel{background:transparent}
.lfile-codewrap[data-live="mermaid"].cw-mm-editing .cw-mm-inplace>:is(rect,circle,ellipse,polygon,path):not(.cw-mm-selbg,.cw-mm-hlbg){stroke:var(--cds-fill-accent,#2a78d6)!important;stroke-width:2px!important}
.lfile-codewrap[data-live="mermaid"].cw-mm-editing g.edgeLabel.cw-mm-inplace foreignObject>div{outline:2px solid var(--cds-fill-accent,#2a78d6);outline-offset:1px;border-radius:2px}
.lfile-codewrap[data-live="mermaid"].cw-mm-editing .cw-mm-inplace :is(p,span,text,tspan){visibility:hidden}
.lfile-codewrap[data-live="mermaid"] .cw-mm-hl{cursor:pointer}
.lfile-codewrap[data-live="mermaid"] .cw-render g.node:hover>:is(rect,circle,ellipse,polygon,path):not(.cw-mm-selbg,.cw-mm-hlbg){stroke:var(--cds-fill-accent,#2a78d6)!important;stroke-width:2px!important}
.lfile-codewrap[data-live="mermaid"] .cw-mm-hl:not(.cw-mm-part-hl)>:is(rect,circle,ellipse,polygon,path):not(.cw-mm-selbg,.cw-mm-hlbg),.lfile-codewrap[data-live="mermaid"] .cw-mm-hl:not(.cw-mm-part-hl)>.cw-mm-person>.cw-mm-person-tile{stroke:${t.rest}!important;stroke-width:2px!important}
.lfile-codewrap[data-live="mermaid"] .cw-mm-hl.cw-res:not(.cw-mm-part-hl)>:is(rect,circle,ellipse,polygon,path):not(.cw-mm-selbg,.cw-mm-hlbg){stroke:${n(60)}!important}
.lfile-codewrap[data-live="mermaid"] .cw-mm-txt-hl{background:${g.rest};border-radius:2px}
.lfile-codewrap[data-live="mermaid"] .cw-mm-hl.cw-on .cw-mm-txt-hl{background:${g.on}}
.lfile-codewrap[data-live="mermaid"] .cw-mm-hl.cw-res .cw-mm-txt-hl{background:${g.res}}
.lfile-codewrap[data-live="mermaid"] .cw-mm-hl.cw-res.cw-on .cw-mm-txt-hl{background:${g.resOn}}
.lfile-codewrap[data-live="mermaid"] .cw-mm-error{display:block;text-align:left;font-family:monospace;white-space:pre-wrap;font-size:var(--cds-font-size-footnote,12px);color:var(--cds-text-danger,#c65949)}
.lfile-codewrap.cw-stale .cw-render{opacity:.45}
.lfile-codewrap.cw-mm-held .cw-render{opacity:.72;transition:opacity .12s}
.lfile-codewrap.cw-mm-held .cw-status{display:inline-flex;color:var(--cds-text-secondary,#6b6a65)}
.lfile-codewrap.cw-mm-held.cw-src-open .cw-errbar{display:block;color:var(--cds-text-secondary,#6b6a65)}
.lfile-codewrap.cw-renderable.cw-src-open{border:${F}px solid var(--cds-border-strong,#b8b6af);border-radius:8px}
.lfile-codewrap.cw-renderable.cw-src-open pre{border-top:${U}px solid var(--cds-border-strong,#b8b6af);background:rgba(0,0,0,.035);border-radius:0 0 8px 8px;padding:12px 16px;min-height:2.2em;tab-size:2;caret-color:var(--cds-text-accent,#4a7cd1)}
[data-mode=dark] .lfile-codewrap.cw-renderable.cw-src-open pre{background:rgba(255,255,255,.04)}
.lfile-codewrap.cw-renderable.cw-src-open pre code{display:block;line-height:1.55}
@media screen{.lfile-codewrap.cw-renderable.cw-src-open>pre{padding-top:${36-U}px}}
.lfile-codewrap .cw-lead{position:absolute;top:0;left:4px;height:24px;z-index:2;display:none;align-items:center;gap:6px;max-width:72%}
.lfile-codewrap.cw-renderable .cw-lead{display:inline-flex}
.lfile-codewrap .cw-srcbtn{box-sizing:border-box;display:inline-flex;align-items:center;gap:3px;height:20px;margin:0;padding:0 6px 0 3px;border:0;border-radius:var(--cds-radius,6px);background:none;font:inherit;font-size:var(--cds-font-size-caption,11px);line-height:1;color:var(--cds-text-secondary,#6b6a63);cursor:pointer;user-select:none;-webkit-user-select:none}
@media (hover:hover){.lfile-codewrap .cw-srcbtn:hover:not(:disabled){background:var(--cds-surface-2,#f2f0ea);color:inherit}}
.lfile-codewrap .cw-srcbtn:focus-visible{outline:2px solid transparent;outline-offset:1px;box-shadow:var(--cds-focus-shadow,0 0 0 2px var(--cds-fill-accent,#2a78d6))}
.lfile-codewrap{--objmenu-top:3px;--objmenu-inset-top:${H}px;--objmenu-inset-right:6px}
.lfile-codewrap.cw-renderable{--objmenu-top:-2px;--objmenu-inset-top:-2px;--objmenu-inset-right:8px}
${A(`.lfile-codewrap[${D}] .cw-head`,`right:38px`)}
${A(`.lfile-codewrap.cw-renderable[${D}] .cw-head`,`right:40px`)}
@media (pointer:coarse){${A(`.lfile-codewrap[${D}] .cw-head`,`right:50px`)}${A(`.lfile-codewrap.cw-renderable[${D}] .cw-head`,`right:52px`)}}
.lfile-codewrap .cw-copy{all:revert-layer;box-sizing:border-box;display:none;flex:none;align-items:center;justify-content:center;width:24px;height:24px;min-width:0;min-height:0;max-width:none;max-height:none;margin:${(z-24)/2}px 0;padding:0;border-width:0;user-select:none;-webkit-user-select:none}
.lfile-codewrap .cw-copy::before,.lfile-codewrap .cw-copy::after,.lfile-codewrap .cw-copy *::before,.lfile-codewrap .cw-copy *::after{all:revert-layer}
.lfile-codewrap .cw-copy .cw-copy-mount,.lfile-codewrap .cw-copy .cw-copy-mount *{all:revert-layer}
.lfile-codewrap .cw-copy .cw-copy-mount{display:contents}
.lfile-codewrap .cw-copy ${I}{width:24px;height:24px;min-width:auto;min-height:auto;max-width:none;max-height:none;margin:0;padding:0;border-width:0}
.lfile-codewrap .cw-copy ${I}:focus-visible{outline:2px solid transparent;outline-offset:1px;box-shadow:var(--cds-focus-shadow,0 0 0 2px var(--cds-fill-accent,#2a78d6))}
@media screen and (hover:hover){.lfile-codewrap[${D}]${L} .cw-copy:not([hidden]){display:inline-flex}}
.lfile-codewrap.cw-src-open :is(.cw-head,.cw-lead){pointer-events:none}
.lfile-codewrap.cw-src-open :is(.cw-head,.cw-lead)>*{pointer-events:auto}
.lfile-codewrap .cw-srcbtn:disabled{opacity:.45;cursor:default}
.lfile-codewrap .cw-srcbtn .cw-chev{flex:none;width:10px;height:10px;transition:transform .12s ease}
${r(`.lfile-codewrap .cw-srcbtn .cw-chev`)}{width:20px;height:20px}
.lfile-codewrap .cw-srcbtn[aria-expanded=true] .cw-chev{transform:rotate(90deg)}
.lfile-codewrap .cw-status{display:none;align-items:center;gap:6px;min-width:0;font-size:var(--cds-font-size-caption,11px);color:var(--cds-text-danger,#c65949)}
.lfile-codewrap.cw-broken .cw-status{display:inline-flex}
.lfile-codewrap .cw-saved-tag{display:none;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;user-select:none;-webkit-user-select:none}
.lfile-codewrap.cw-shows-saved .cw-saved-tag{display:inline}
.lfile-codewrap .cw-status .msg{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.lfile-codewrap .cw-status button{flex:none;font-size:inherit;color:inherit;background:none;border:1px solid currentColor;border-radius:var(--cds-radius,6px);padding:0 6px;cursor:pointer}
.lfile-codewrap :is(.cw-render.cw-empty,.cw-saved-tag){color:var(--cds-text-secondary,#6b6a65);font-size:var(--cds-font-size-footnote,12px)}
.lfile-codewrap.cw-src-open .cw-render.cw-empty{display:none}
.lfile-codewrap .cw-errbar{display:none;font-size:var(--cds-font-size-caption,11px);color:var(--cds-text-danger,#c65949);padding:3px 8px;border-top:1px solid var(--cds-border-strong,#b8b6af);cursor:pointer}
.lfile-codewrap.cw-broken .cw-errbar{display:block}
.cw-err-char{text-decoration:underline wavy;text-decoration-color:var(--cds-text-danger,#c65949);text-underline-offset:2px}
.lfile-codewrap.cw-renderable:not(.cw-src-open) pre{display:none}
.lfile-codewrap .cw-src-copy{display:none}
.lfile-codewrap.cw-renderable.cw-shows-saved:not(.cw-src-open) .cw-src-copy{display:block;border-top:${U}px solid var(--cds-border-strong,#b8b6af);padding:12px 16px;font:.875em/1.55 ${f};tab-size:2;white-space:pre-wrap;overflow-wrap:anywhere;user-select:none;-webkit-user-select:none;cursor:default}
.lfile-codewrap.cw-renderable.ProseMirror-selectednode{box-shadow:0 0 0 2px var(--cds-fill-accent,#2a78d6)}
[data-lfile-composing] .ProseMirror:not(.ProseMirror-focused) .lfile-codewrap.cw-renderable.ProseMirror-selectednode{box-shadow:0 0 0 2px ${i}}
.ProseMirror-hideselection .lfile-codewrap ::selection{color:currentcolor;background-color:transparent}
.lfile-codewrap[data-code-comment-whole]{outline:2px solid ${t.rest};outline-offset:3px;border-radius:8px}
.lfile-codewrap[data-code-comment-whole=res]{outline-color:${n(40)}}
.lfile-codewrap[data-code-comment-active=focus]{outline:2px solid var(--cds-fill-accent,#2a78d6);outline-offset:3px;border-radius:8px}
.lfile-codewrap[data-code-comment-active=hover]{outline:2px solid color-mix(in srgb,var(--cds-fill-accent,#2a78d6) 50%,transparent);outline-offset:3px;border-radius:8px}
.lfile-codewrap[data-code-comment-active=hover] .cw-render{background:${v(8)}}
.lfile-codewrap[data-code-comment-active=focus] .cw-render{background:${v(15)}}
.lfile-codewrap.cw-ring-res[data-code-comment-active]{outline-color:${n(60)}}
`,G=()=>{let e=d();return e.locale===void 0?e.uiLocale:void 0},K=new Set([`gregory`,`buddhist`,`japanese`,`roc`]),q=e=>G()===void 0||K.has(new Intl.DateTimeFormat(e).resolvedOptions().calendar)?{}:{calendar:`gregory`},oe=new Map,se=new Map,J=e=>{let t=G()===void 0?oe:se,n=t.get(e);return n===void 0&&(n=new Intl.DateTimeFormat(e,{timeZone:`UTC`,month:`short`,day:`numeric`,year:`numeric`,...q(e)}),t.set(e,n)),n},Y=e=>{if(!e)return`Pick date`;let t=new Date(`${e}T00:00:00Z`);return Number.isNaN(+t)||t.getUTCFullYear()<1?e:J(p(`DateTimeFormat`,d())).format(t)},X=e=>{let t=/^(\d{4}-\d{2}-\d{2})(?:T(\d{2}:\d{2})(?:\[([^\]]+)\])?)?$/.exec(e);return t?{date:t[1],time:t[2],zone:t[3]}:{date:e.slice(0,10)}},ce=e=>{let t=new Date(`2000-01-01T${e}:00Z`);return Number.isNaN(+t)?e:t.toLocaleTimeString(p(`DateTimeFormat`,d()),{timeZone:`UTC`,hour:`numeric`,minute:`2-digit`})},le=(e,t,n)=>{try{let r=new Intl.DateTimeFormat(`en-US`,{timeZone:e,timeZoneName:`short`,year:`numeric`,month:`numeric`,day:`numeric`,hour:`numeric`,minute:`numeric`,hourCycle:`h23`}),i=e=>{let t=r.formatToParts(new Date(e)),n=e=>Number(t.find(t=>t.type===e)?.value);return Date.UTC(n(`year`),n(`month`)-1,n(`day`),n(`hour`),n(`minute`))-e},a=Date.parse(`${t}T${n}:00Z`),o=a-i(a-i(a));return r.formatToParts(new Date(o)).find(e=>e.type===`timeZoneName`)?.value??null}catch{return null}},ue=e=>{if(!e)return Y(``);let{date:t,time:n,zone:r}=X(e),i=Y(t);if(n===void 0)return i;let a=ce(n);if(r===void 0)return`${i} ${a}`;let o=le(r,t,n);return o===null?`${i} ${a}`:`${i} ${a} ${o}`},de=(e=typeof navigator>`u`?``:navigator.userAgent)=>/gecko\/\d/i.test(e)?void 0:`auto`,Z=s.slice(1),Q=e=>Z[e%Z.length],fe=e=>_[Q(e)].strong,$=(e,t)=>o(e.color)??Q(t),pe=(e,t)=>_[$(e,t)].strong;export{k as _,ue as a,te as b,G as c,T as d,E as f,O as g,N as h,fe as i,R as l,w as m,pe as n,X as o,D as p,$ as r,q as s,de as t,W as u,C as v,ee as y};