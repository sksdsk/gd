import fs from 'node:fs/promises';
import * as T from '../vendor/three.module.min.js';
import {GLTFExporter} from '../vendor/GLTFExporter.js';
import {mergeGeometries} from '../vendor/BufferGeometryUtils.js';

// Node-only export shim. No browser, canvas, network or external textures required.
globalThis.FileReader=class {readAsArrayBuffer(b){b.arrayBuffer().then(r=>{this.result=r;this.onloadend?.();});}readAsDataURL(b){b.arrayBuffer().then(r=>{this.result=`data:${b.type};base64,${Buffer.from(r).toString('base64')}`;this.onloadend?.();});}};
const config=JSON.parse(await fs.readFile(new URL('../site-config.json',import.meta.url),'utf8'));
const d=config.dimensions,L=d.envelopeLength,W=d.envelopeWidth,A=d.planterCourtDepth,B=L-d.bareCourtDepth,S=d.sideStripWidth;
const scene=new T.Scene();scene.name='Wuhan_Existing_Site_R1';scene.userData={status:config.status,units:'metres',north:'-X',east:'-Z',dimensionStatus:config.dimensionStatus,levelStatus:config.groundLevels};
const mats={};for(const [key,color] of Object.entries({soil:'#a39d7e',beds:'#b2b2aa',brick:'#ac6d58',brickBlue:'#697b80',gravel:'#c8c8c1',slab:'#b7b8b1',stone:'#e0dbcc',dark:'#505552',metal:'#66534b',glass:'#73888e',plant:'#73806a',pipe:'#d1c8ac',yellow:'#bd964c',wall:'#ddd7ca',threshold:'#ada99b'}))mats[key]=new T.MeshStandardMaterial({name:key,color,roughness:key==='glass'?.35:.88,metalness:key==='metal'?.3:0});
const groups={};function group(name,feature,parent=scene){const g=new T.Group();g.name=name;g.userData={feature,geometry:'UNMEASURED_PROXY'};parent.add(g);groups[name]=g;return g;}
function box(g,n,x,y,z,w,h,dep,mat){const m=new T.Mesh(new T.BoxGeometry(w,h,dep),mats[mat]);m.position.set(x,y,z);m.name=n;g.add(m);return m;}
function rod(g,n,a,b,r,mat){const av=new T.Vector3(...a),bv=new T.Vector3(...b),v=bv.clone().sub(av);const m=new T.Mesh(new T.CylinderGeometry(r,r,v.length(),6),mats[mat]);m.position.copy(av.add(bv).multiplyScalar(.5));m.quaternion.setFromUnitVectors(new T.Vector3(0,1,0),v.normalize());m.name=n;g.add(m);return m;}
function merge(g){const sets=new Map();for(const m of [...g.children]){if(!m.isMesh)continue;m.updateMatrix();let ge=m.geometry.clone().applyMatrix4(m.matrix);if(!sets.has(m.material))sets.set(m.material,[]);sets.get(m.material).push(ge);g.remove(m);m.geometry.dispose();}for(const [mat,geos]of sets){const mesh=new T.Mesh(mergeGeometries(geos),mat);mesh.name=g.name+'_'+mat.name;g.add(mesh);geos.forEach(x=>x.dispose());}}
const terrain=group('Terrain_Flattened_Unknown_Levels','paving');box(terrain,'R0_Flat_Datum',L/2,-.16,W/2,L,.28,W,'soil');
const z1=group('Zone_1_Planter_Courtyard','zone1');box(z1,'Unpaved_Ground',A/2,-.008,W/2,A-.08,.02,W-.08,'soil');
const z2=group('Zone_2_Bare_Courtyard','zone2');box(z2,'Bare_Soil_Not_New_Lawn',(B+L)/2,-.004,W/2,L-B-.08,.025,W-.08,'soil');
const ar=group('Architecture_Low_Footprint_Proxy','architecture');box(ar,'Footprint_Proxy_Unsurveyed',(A+B)/2,.2,(S+W)/2,B-A,.4,W-S,'stone');
const full=group('Architecture_Upper_Proxy','architecture');box(full,'Unsurveyed_Building_Mass',(A+B)/2,(d.buildingHeight+.4)/2,(S+W)/2,B-A,d.buildingHeight-.4,W-S,'stone');
// Visible openings only: simplified placeholders; no hidden windows or interiors.
for(const [side,x]of [['planter',A-.025],['bare',B+.025]]){
 const g=group('Visible_'+side+'_Openings','architecture',full);
 const dirs=side==='planter'?[7.8,8.8]:[4.1,7.5];
 for(let i=0;i<dirs.length;i++){const z=dirs[i];box(g,'Ground_Opening_'+i,x,1.65,z,.07,2.55,i===0?1.8:1.45,'dark');box(g,'Glazing_'+i,x+(side==='planter'?-.04:.04),1.65,z,.04,2.35,i===0?1.6:1.25,'glass');}
 if(side==='bare'){box(g,'Balcony_Slab_Visible',x+.42,3.35,4.2,.9,.18,3.2,'stone');box(g,'Balcony_Dark_Recess',x+.02,4.6,4.2,.08,2.3,3.1,'dark');for(let z=2.7;z<5.8;z+=.2)box(g,'Balcony_Rail',x+.87,3.95,z,.04,1.04,.025,'metal');}
 merge(g);
}
const services=group('Wall_Services_Visible_Proxies','services');
box(services,'Side_Louvre_Unmeasured',(A+B)/2,1.9,S-.02,3.3,1.8,.08,'dark');for(let y=1.12;y<2.75;y+=.14)box(services,'Louvre_Blade',(A+B)/2,y,S-.075,3.15,.04,.12,'metal');
rod(services,'White_Exposed_Pipe',[A-.13,.1,8.12],[A-.13,3.5,8.12],.055,'pipe');rod(services,'Yellow_Pipe_Function_Unverified',[A-.15,.12,7.93],[A-.15,2.5,7.93],.024,'yellow');
box(services,'Grey_Facade_Panel_Function_Unverified',A-.18,.42,8.75,.08,.8,1.08,'slab');merge(services);
const pave=group('Existing_Paving_Simplified','paving');
// Red paved apron around the two beds. Individual joints are indicative only.
const brickRegion={x0:.15,x1:A-.1,z0:.15,z1:3.95};
box(pave,'Red_Brick_Mortar_Base',A/2,.02,2.05,A-.25,.04,3.8,'brick');
const bricks=group('Red_Brick_Joints_Indicative','paving',pave);
for(let row=0,z=.15;z<3.89;z+=.13,row++)for(let x=.15+(row%2)*.12;x<A-.12;x+=.245){const w=Math.min(.232,A-.1-x);if(w>.035)box(bricks,'Brick',x+w/2,.046,z+.058,w,.026,.116,(row%9===0&&Math.round(x*10)%5===0)?'brickBlue':'brick');}
merge(bricks);
box(pave,'Grey_Access_Route_Approximate',A/2,.028,d.mainRouteZ,A-.08,.055,d.mainRouteWidth,'slab');
box(pave,'Facade_Access_Approximate',A-.38,.029,7.25,.7,.056,3.4,'slab');
const pass=group('Zone_3_Steps_And_Gravel','passage');box(pass,'Gravel_Path',(A+B)/2,.015,.94,B-A+3.6,.035,.88,'gravel');
for(let x=A-1.4;x<B+1.6;x+=.89)box(pass,'Existing_Square_Slab',x,.045,.94,d.pathSlabLength,.065,d.pathSlabWidth,'slab');
box(pass,'Narrow_Brick_Edge_Outside',(A+B)/2,.04,.47,B-A+3.6,.055,.075,'brick');box(pass,'Narrow_Brick_Edge_Inside',(A+B)/2,.04,1.41,B-A+3.6,.055,.075,'brick');merge(pass);
const bedStart=.35;
for(let i=0;i<2;i++){
 const z=.53+i*(d.bedWidth+d.bedGap),x=bedStart+d.bedLength/2,w=d.bedWidth,h=d.bedHeight,len=d.bedLength,t=.12;
 const g=group('Concrete_Planter_P'+(i+1),'bed'+(i+1));
 box(g,'Long_Wall_Outer',x,h/2+.065,z+t/2,len,h,t,'beds');box(g,'Long_Wall_Inner',x,h/2+.065,z+w-t/2,len,h,t,'beds');
 box(g,'End_Wall_1',bedStart+t/2,h/2+.065,z+w/2,t,h,w-2*t,'beds');box(g,'End_Wall_2',bedStart+len-t/2,h/2+.065,z+w/2,t,h,w-2*t,'beds');
 box(g,'Soil_Surface_Depth_Unknown',x,h-.025,z+w/2,len-2*t,.045,w-2*t,'soil');g.userData.assumedDimensionsMetres=[len,w,h];g.userData.baseConstruction='UNKNOWN; no structural base modelled';
}
function fence(g,n,x1,z1,x2,z2){const len=Math.hypot(x2-x1,z2-z1),dx=(x2-x1)/len,dz=(z2-z1)/len;for(let s=0;s<=len;s+=.18){const x=x1+dx*s,z=z1+dz*s;rod(g,n+'_Picket',[x,.06,z],[x,1.35,z],.016,'metal');}for(let s=0;s<=len;s+=1.55){const x=x1+dx*s,z=z1+dz*s;rod(g,n+'_Post',[x,.02,z],[x,1.4,z],.032,'metal');}for(const y of [.24,1.32])rod(g,n+'_Rail',[x1,y,z1],[x2,y,z2],.025,'metal');}
const f=group('Boundary_Fences_Approximate','boundary');fence(f,'Side',0,0,L,0);fence(f,'Planter_Outer_1',0,0,0,6.94);fence(f,'Planter_Outer_2',0,8.65,0,W);fence(f,'Bare_Outer_1',L,0,L,5.7);fence(f,'Bare_Outer_2',L,6.9,L,W);fence(f,'Bare_Divider',B,W,L,W);fence(f,'Planter_Divider',0,W,A,W);merge(f);
const gate=group('Gates_And_Low_Walls_Approximate','boundary');box(gate,'Gate_Pier_Left',0,.73,6.95,.22,1.46,.19,'wall');box(gate,'Gate_Pier_Right',0,.73,8.65,.22,1.46,.19,'wall');box(gate,'Low_Wall',0,.43,4.69,.18,.86,2.55,'wall');fence(gate,'Gate_Closed_Reference',0,7.06,0,8.54);box(gate,'Gate_Leaf_Base',0,.38,7.8,.045,.7,1.48,'metal');merge(gate);
const gate2=group('Bare_Court_Gate_Location_Approximate','boundary');box(gate2,'Bare_Gate_Pier_1',L,.75,5.71,.22,1.5,.19,'wall');box(gate2,'Bare_Gate_Pier_2',L,.75,6.89,.22,1.5,.19,'wall');fence(gate2,'Bare_Gate_Closed_Reference',L,5.84,L,6.76);merge(gate2);
const arches=group('Existing_Light_Arches_Schematic','arch');for(const x of [A+.8,A+3,A+5.2]){
 let prev=null;for(let k=0;k<=12;k++){const z=.04+(S-.08)*k/12,y=1.65+.52*Math.sin(Math.PI*k/12);const v=[x,y,z];if(prev)rod(arches,'Arch_Existing',prev,v,.023,'metal');prev=v;}
}merge(arches);
const drain=group('Drain_Visible_Location_Approximate','drain');const dx=L-1.1,dz=6.9;box(drain,'Grate_Opening_No_Pipe_Inferred',dx,.025,dz,.45,.04,.62,'dark');for(let z=dz-.28;z<dz+.3;z+=.07)box(drain,'Grate_Bar',dx,.053,z,.43,.035,.024,'metal');merge(drain);
const plants=group('Existing_Vegetation_Abstract_Cover_Only','vegetation');
for(const z of [1.07,2.63])for(let x=.75;x<4.95;x+=.6){const m=new T.Mesh(new T.IcosahedronGeometry(.39,0),mats.plant);m.scale.set(1.08,.8,1);m.position.set(x,.74,z);m.name='Existing_Cultivation_Unidentified';plants.add(m);}
for(let x=A+.4;x<B-.3;x+=1.35){const m=new T.Mesh(new T.IcosahedronGeometry(.29,0),mats.plant);m.scale.set(.9,.6,1.05);m.position.set(x,.2,1.7);m.name='Existing_Ground_Cover_Unidentified';plants.add(m);}merge(plants);
scene.updateMatrixWorld(true);const result=await new GLTFExporter().parseAsync(scene,{binary:true,onlyVisible:false,trs:true});
const target=new URL('../models/existing-site.glb',import.meta.url);await fs.writeFile(target,Buffer.from(result));
let meshes=0,triangles=0;scene.traverse(o=>{if(o.isMesh){meshes++;triangles+=(o.geometry.index?.count??o.geometry.attributes.position.count)/3;}});
const stats={bytes:result.byteLength,meshes,triangles,groups:Object.keys(groups).length,threeRevision:T.REVISION,status:config.status};await fs.writeFile(new URL('../models/model-stats.json',import.meta.url),JSON.stringify(stats,null,2));console.log(JSON.stringify(stats));
