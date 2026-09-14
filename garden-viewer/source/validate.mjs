import fs from 'node:fs/promises';
import assert from 'node:assert/strict';
import * as T from '../vendor/three.module.min.js';
import {GLTFLoader} from '../vendor/GLTFLoader.js';
const root=new URL('../',import.meta.url),read=async f=>JSON.parse(await fs.readFile(new URL(f,root)));
const layouts=await read('layouts.json'),config=await read('site-config.json');
assert.equal(config.dimensions.planterCourtDepth,7);assert.equal(config.dimensions.bareCourtDepth,8);assert.deepEqual(config.north,[-1,0,0]);
const files=(await fs.readdir(new URL('models/',root))).filter(f=>f.endsWith('.glb'));assert.equal(files.length,10);
const results=[];
for(const file of files){const b=await fs.readFile(new URL('models/'+file,root));assert.equal(b.toString('ascii',0,4),'glTF');assert.equal(b.readUInt32LE(4),2);assert.equal(b.readUInt32LE(8),b.length);const gltf=JSON.parse(b.toString('utf8',20,20+b.readUInt32LE(12)));assert.ok(gltf.materials.length>0);assert.ok(!gltf.images?.some(x=>x.uri));assert.ok(gltf.buffers.every(x=>!x.uri));
 const {scene}=await new GLTFLoader().parseAsync(b.buffer.slice(b.byteOffset,b.byteOffset+b.byteLength),'');scene.updateMatrixWorld(true);const box=new T.Box3().setFromObject(scene.getObjectByName('Architecture_Low_Footprint_Proxy'));assert.ok(Math.abs(box.max.x-box.min.x-10)<.00001);
 const choice=file==='existing-site.glb'?'existing':file==='garden.glb'?'B':file.split('-')[1],expected=choice==='existing'?['P1','P2']:layouts[choice].retainedBeds;
 for(const bed of ['P1','P2'])assert.equal(!!scene.getObjectByName('Concrete_Planter_'+bed),expected.includes(bed),file+' '+bed);
 const groups=[];let vertices=0,triangles=0;
 scene.traverse(o=>{if(o.userData.plantGroup)groups.push(o.userData);if(o.isMesh){for(const val of o.geometry.attributes.position.array)assert.ok(Number.isFinite(val),file+' non-finite position');vertices+=o.geometry.attributes.position.count;triangles+=(o.geometry.index?.count??o.geometry.attributes.position.count)/3;}});
 if(choice!=='existing'){assert.equal(groups.length,layouts[choice].groups.length);for(const group of groups){const match=layouts[choice].groups.find(g=>g.id===group.plantGroup);assert.equal(group.quantity,match.points.length);assert.deepEqual(group.coordinates,match.points);}const counts={};groups.forEach(g=>counts[g.species]=(counts[g.species]??0)+g.quantity);for(const [species,count]of Object.entries(layouts[choice].quantities))if(species!=='ZJ')assert.equal(counts[species],count);}
 results.push({file,bytes:b.length,triangles,plantGroups:groups.length,status:'passed'});
 const geometries=new Set(),materials=new Set();scene.traverse(o=>{if(o.isMesh){geometries.add(o.geometry);materials.add(o.material);}});geometries.forEach(g=>g.dispose());materials.forEach(m=>m.dispose());
}
await fs.writeFile(new URL('models/validation.json',root),JSON.stringify({checks:'GLB 2.0 decoded using Three.js; finite geometry; 10m architectural footprint; planter alternatives; plant coordinates and counts; embedded resources',browserOrDeviceTests:false,models:results},null,2));console.log(JSON.stringify(results));
