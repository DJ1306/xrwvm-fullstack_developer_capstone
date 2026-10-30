const {MongoMemoryServer}=require('mongodb-memory-server');
const path=require('node:path'),fs=require('node:fs');
const {start}=require('./app');
(async()=>{
 const dbPath=path.join(__dirname,'.mongo');fs.mkdirSync(dbPath,{recursive:true});
 const mongo=await MongoMemoryServer.create({binary:{version:'7.0.14'},instance:{dbPath,storageEngine:'wiredTiger'}});
 const server=await start(mongo.getUri());
 async function close(){server.close();await mongo.stop();process.exit(0);}
 process.on('SIGINT',close);process.on('SIGTERM',close);
})().catch(err=>{console.error(err);process.exit(1);});
