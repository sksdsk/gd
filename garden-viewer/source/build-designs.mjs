import fs from 'node:fs/promises';
import * as T from '../vendor/three.module.min.js';
import {GLTFLoader} from '../vendor/GLTFLoader.js';
import {GLTFExporter} from '../vendor/GLTFExporter.js';
import {mergeGeometries} from '../vendor/BufferGeometryUtils.js';
globalThis.FileReader=class{readAsArrayBuffer(b){b.arrayBuffer().then(r=>{this.result=r;this.onloadend?.();});}readAsDataURL(b){b.arrayBuffer().then(r=>{this.result=`data:${b.type};base64,${Buffer.from(r).toString('base64')}`;this.onloadend?.();});}};
const base=new URL('../',import.meta.url);
const plants=JSON.parse(await fs.readFile(new URL('plants.json',base)));
const layouts=JSON.parse(await fs.readFile(new URL('layouts.json',base)));
const bytes=await fs.readFile(new URL('models/existing-site.glb',base));
const existing=(await new GLTFLoader().parseAsync(bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength),'')).scene;
const mats={};
function material(key,color){return mats[key]??=(new T.MeshStandardMaterial({name:key,color,roughness:.88,side:T.DoubleSide}));}
const bark=material('Bark','#786957'),mulch=material('Organic_Mulch','#8c8269'),pathmat=material('New_Warm_Grey_Paving','#c4c2b4');
const soil=material('Repaired_Planter_Soil','#928971'),white=material('White_Flower','#eee9df'),purple=material('Violet_Flower','#9a90ba');
function group(parent,name,data={}){const g=new T.Group();g.name=name;g.userData=data;parent.add(g);return g;}
function mesh(parent,geo,mat,pos=[0,0,0],scale=[1,1,1]){const m=new T.Mesh(geo,mat);m.position.set(...pos);m.scale.set(...scale);parent.add(m);return m;}
function rod(parent,a,b,r=.018){const aa=new T.Vector3(...a),bb=new T.Vector3(...b),v=bb.clone().sub(aa);const m=mesh(parent,new T.CylinderGeometry(r*.6,r,v.length(),5),bark,aa.add(bb).multiplyScalar(.5).toArray());m.quaternion.setFromUnitVectors(new T.Vector3(0,1,0),v.normalize());}
function merge(g){const sets=new Map();for(const m of [...g.children]){if(!m.isMesh)continue;m.updateMatrix();let geo=m.geometry.clone().applyMatrix4(m.matrix);if(geo.index)geo=geo.toNonIndexed();geo.deleteAttribute('uv');geo.normalizeNormals();(sets.get(m.material)??sets.set(m.material,[]).get(m.material)).push(geo);g.remove(m);m.geometry.dispose();}for(const [mat,gs]of sets){const m=mesh(g,mergeGeometries(gs),mat);m.name=g.name+'_'+mat.name;gs.forEach(x=>x.dispose());}}
function polygon(parent,points,mat,y=.071){const s=new T.Shape();points.forEach(([x,z],i)=>i?s.lineTo(x,-z):s.moveTo(x,-z));s.closePath();const ge=new T.ShapeGeometry(s);ge.rotateX(-Math.PI/2);const m=mesh(parent,ge,mat,[0,y,0]);return m;}
function route(parent,points,width){for(let i=1;i<points.length;i++){const [x0,z0]=points[i-1],[x1,z1]=points[i],dx=x1-x0,dz=z1-z0,len=Math.hypot(dx,dz),nx=-dz/len*width/2,nz=dx/len*width/2;polygon(parent,[[x0+nx,z0+nz],[x1+nx,z1+nz],[x1-nx,z1-nz],[x0-nx,z0-nz]],pathmat,.074);}
 for(const[x,z]of points){if(x===17||x===25)continue;const ge=new T.CircleGeometry(width/2,12);ge.rotateX(-Math.PI/2);mesh(parent,ge,pathmat,[x,.074,z]);}}
let seed=3;function rnd(){seed=(1664525*seed+1013904223)>>>0;return seed/4294967296;}
function leaves(parent,pos,h,w,code){const mat=material('Foliage_'+code,plants[code].color);const count=code==='LM'?12:code==='IT'?7:6;const verts=[];
 for(let i=0;i<count;i++){const a=i/count*Math.PI*2+rnd()*.35,reach=w*(.36+rnd()*.12),hh=h*(.8+rnd()*.2),half=code==='AS'?w*.085:code==='IT'?w*.055:w*.022;
  const p=[];for(let j=0;j<5;j++){const t=j/4,r=reach*t,yy=hh*Math.sin(t*Math.PI*.72),ww=half*Math.sin(Math.PI*t)*.95;for(const side of [-1,1])p.push([pos[0]+Math.cos(a)*r-Math.sin(a)*ww*side,pos[1]+yy,pos[2]+Math.sin(a)*r+Math.cos(a)*ww*side]);}
  for(let j=0;j<4;j++){const k=j*2;for(const n of [k,k+1,k+2,k+1,k+3,k+2])verts.push(...p[n]);}
 }
 const ge=new T.BufferGeometry();ge.setAttribute('position',new T.Float32BufferAttribute(verts,3));ge.computeVertexNormals();mesh(parent,ge,mat);
}
function woody(parent,stemParent,flowers,pos,h,w,code){const foliage=material('Foliage_'+code,plants[code].color),light=material('Foliage_Light_'+code,new T.Color(plants[code].color).lerp(new T.Color('#b3b78a'),.14));const tree=plants[code].kind==='tree',trunk=tree?h*.43:h*.14;
 rod(stemParent,pos,[pos[0],pos[1]+trunk,pos[2]],tree?.048:.013);
 const clusters=tree?12:9;
 for(let j=0;j<clusters;j++){const a=j*2.399,rad=Math.sqrt((j+.5)/clusters)*w*.32,xx=pos[0]+Math.cos(a)*rad,zz=pos[2]+Math.sin(a)*rad,yy=pos[1]+trunk+(h-trunk)*(.30+.39*rnd());const end=[xx,yy,zz];
  rod(stemParent,[pos[0],pos[1]+trunk*.6,pos[2]],end,tree?.018:.008);
  mesh(parent,new T.IcosahedronGeometry(1,1),j%3?foliage:light,end,[w*.23,(h-trunk)*.32,w*.23]);
  if(flowers&&j%2===0){for(let f=0;f<3;f++){const ff=[xx+(rnd()-.5)*w*.25,yy+(h-trunk)*.28,zz+(rnd()-.5)*w*.25];mesh(flowers,new T.IcosahedronGeometry(1,0),white,ff,code==='HY'?[.12,.08,.12]:code==='LI'?[.065,.14,.065]:[.035,.03,.035]);}}
 }
}
const allstats=[];
for(const opt of ['A','B','C'])for(const year of [1,3,5]){
 seed=1107;const layout=layouts[opt],scene=new T.Scene();scene.name=`Wuhan_Design_${opt}_Year_${year}`;
 scene.userData={units:'metres',north:'-X',east:'-Z',design:opt,year,season:'summer',growth:'Managed illustrative envelopes, not predicted growth; seasonal tags in extras',survey:'R1 annotated envelope, unmeasured local geometry',recommended:opt==='B',coordinates:'Plant schedule uses X=south, Z=west; origin NE corner'};
 const site=existing.clone(true);site.name='Existing_Architecture_And_Hardscape';scene.add(site);
 site.getObjectByName('Existing_Vegetation_Abstract_Cover_Only')?.removeFromParent();
 for(const id of ['P1','P2'])if(!layout.retainedBeds.includes(id))site.getObjectByName('Concrete_Planter_'+id)?.removeFromParent();
 // C removes the brick geometry within a rectangular subgrade opening, rather than burying it.
 if(opt==='C'){
  site.getObjectByName('Red_Brick_Mortar_Base')?.removeFromParent();
  const bricks=site.getObjectByName('Red_Brick_Joints_Indicative');
  bricks?.traverse(o=>{if(!o.isMesh)return;const src=o.geometry.index?o.geometry.toNonIndexed():o.geometry;const pos=src.attributes.position,nor=src.attributes.normal,uv=src.attributes.uv,pp=[],nn=[],uu=[];
   for(let i=0;i<pos.count;i+=3){const x=(pos.getX(i)+pos.getX(i+1)+pos.getX(i+2))/3,z=(pos.getZ(i)+pos.getZ(i+1)+pos.getZ(i+2))/3;if(x>=.35&&x<=5.15&&z>=.45&&z<=3.45)continue;for(let j=0;j<3;j++){pp.push(pos.getX(i+j),pos.getY(i+j),pos.getZ(i+j));nn.push(nor.getX(i+j),nor.getY(i+j),nor.getZ(i+j));if(uv)uu.push(uv.getX(i+j),uv.getY(i+j));}}
   const ge=new T.BufferGeometry();ge.setAttribute('position',new T.Float32BufferAttribute(pp,3));ge.setAttribute('normal',new T.Float32BufferAttribute(nn,3));if(uv)ge.setAttribute('uv',new T.Float32BufferAttribute(uu,2));o.geometry=ge;
  });
 }
 // Existing paving stays except explicit C cutout; B gets a matching brick repair at P2.
 const paving=group(scene,'Proposed_Paths_And_Repairs',{feature:'paving'});
 polygon(paving,[[17.05,2.1],[17.7,2.1],[17.7,9.9],[17.05,9.9]],material('Service_Gravel','#b7b5a6'),.023);
 if(opt==='B'){const repair=group(paving,'P2_Footprint_Local_Brick_Repair',{feature:'bed2'});polygon(repair,[[.35,2.09],[5.15,2.09],[5.15,3.17],[.35,3.17]],material('Salvaged_Red_Brick','#ad7661'),.066);for(let x=.4;x<5.1;x+=.25){const m=mesh(repair,new T.BoxGeometry(.008,.003,1.04),soil,[x,.069,2.63]);}merge(repair);}
 const planting=group(scene,'Proposed_Planting_Beds_And_Mulch',{feature:'vegetation'});
 if(opt==='C')polygon(planting,[[.35,.45],[5.15,.45],[5.15,3.45],[.35,3.45]],mulch,.055);
 // Flat top surfaces only; specified build-up and fall require site levels.
 polygon(planting,[[.12,4.05],[6.5,4.05],[6.5,6.96],[.12,6.96]],mulch,.018);
 polygon(planting,[[.12,8.65],[6.5,8.65],[6.5,9.88],[.12,9.88]],mulch,.018);
 polygon(planting,[[17.05,.08],[24.92,.08],[24.92,9.92],[17.05,9.92]],mulch,.018);
 for(const s of layout.surfaces){const g=group(planting,s.id,{surface:s.id,area:s.area,feature:s.kind==='turf'?'turf':'vegetation'});polygon(g,s.polygon,s.kind==='turf'?material('Turf_Green',plants.ZJ.color):mulch,s.id==='N-low-border'?.069:.03);if(s.kind==='turf')g.userData.seasonalTurf=true;}
 // No invented drain pipes. Grate stays visible and reachable.
 const drain=site.getObjectByName('Drain_Visible_Location_Approximate');drain.position.y=.065;
 polygon(paving,[[23.45,6.42],[24.4,6.42],[24.4,7.4],[23.45,7.4]],pathmat,.072);
 for(const p of layout.paths){const g=group(paving,p.id,{feature:'newpaths',width:p.width});route(g,p.points,p.width);merge(g);}
 const plantsRoot=group(scene,'Plants_By_Zone_And_Cohort');
 const categories={};for(const zone of [1,2,3])categories[zone]=group(plantsRoot,'Zone_'+zone+'_Planting');
 for(const c of layout.groups){const p=plants[c.species],sz=p.sizes[year];const g=group(categories[c.zone],`${c.id}_${c.species}_${c.quantity}_plants`,{plantGroup:c.id,species:c.species,quantity:c.quantity,zone:c.zone,commonName:p.name,botanicalName:p.botanical,matureSize:p.mature,flowering:p.flower,sun:p.light,water:p.water,maintenance:p.care,spacing:p.spacing,coordinates:c.points,designEnvelope:sz,source:p.source});
  const stem=group(g,'Branches_'+c.id),leaf=group(g,'Leaves_'+c.id,{leafType:p.evergreen?'evergreen':c.species==='AB'?'semi-evergreen':'deciduous',species:c.species});
  const flower=p.bloom.length?group(g,'Flowers_'+c.id,{flowerSeasons:p.bloom}):null;
  for(const [x,z]of c.points){const h=sz[0],w=sz[1],pos=[x,c.base+.035,z];
   if(['grass','leaf','iris'].includes(p.kind)){leaves(leaf,pos,h,w,c.species);if(flower){rod(stem,pos,[x,pos[1]+h*1.15,z],.004);mesh(flower,new T.IcosahedronGeometry(1,0),purple,[x,pos[1]+h*1.15,z],[.045,.055,.045]);}}
   else if(p.kind==='climber'){
    const alongZ=c.id==='S07';const support=group(g,'Selective_Vine_Support_'+c.id);for(const side of [-1,1]){const xx=x+(alongZ?0:side*.72),zz=z+(alongZ?side*.72:0);rod(support,[xx,.05,zz],[xx,1.95,zz],.014);}merge(support);
    for(let j=0;j<8;j++){const along=(j%3-1)*w*.34,xx=x+(alongZ?0:along),zz=z+(alongZ?along:0),yy=.28+(j/8)*h;mesh(leaf,new T.IcosahedronGeometry(1,1),material('Foliage_TJ',p.color),[xx,yy,zz],alongZ?[.17,h*.18,w*.27]:[w*.27,h*.18,.17]);if(flower&&j%2===0)mesh(flower,new T.IcosahedronGeometry(.035,0),white,[xx,yy+.12,zz-.12]);}
   }else woody(leaf,stem,flower,pos,h,w,c.species);
  }
  merge(stem);merge(leaf);if(flower){merge(flower);flower.scale.setScalar(p.bloom.includes('summer')?1:0);}
 }
 // Materials, all seasonal states and semantic metadata are embedded; no image dependencies.
 scene.updateMatrixWorld(true);const output=await new GLTFExporter().parseAsync(scene,{binary:true,onlyVisible:false,trs:true});
 const file=opt==='B'&&year===3?'garden.glb':`design-${opt}-year${year}.glb`;
 await fs.writeFile(new URL('models/'+file,base),Buffer.from(output));
 let triangles=0,meshes=0;scene.traverse(o=>{if(o.isMesh){meshes++;triangles+=(o.geometry.index?.count??o.geometry.attributes.position.count)/3;}});allstats.push({file,design:opt,year,bytes:output.byteLength,triangles,meshes});
 console.log(file,(output.byteLength/1048576).toFixed(2)+' MiB',triangles+' triangles');
}
await fs.writeFile(new URL('models/design-stats.json',base),JSON.stringify(allstats,null,2));
