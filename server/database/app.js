const express=require('express'),mongoose=require('mongoose'),fs=require('node:fs'),path=require('node:path');
const Reviews=require('./review'),Dealers=require('./dealership');
const app=express();app.use(require('cors')());app.use(express.json({limit:'100kb'}));
const safe=fn=>(req,res,next)=>Promise.resolve(fn(req,res,next)).catch(next);
app.get('/',(req,res)=>res.json({service:'Dealership API',status:'ready'}));
app.get('/fetchReviews',safe(async(req,res)=>res.json(await Reviews.find().select('-_id -__v').lean())));
app.get('/fetchReviews/dealer/:id',safe(async(req,res)=>res.json(await Reviews.find({dealership:req.params.id}).select('-_id -__v').lean())));
app.get('/fetchDealers',safe(async(req,res)=>res.json(await Dealers.find().sort({id:1}).select('-_id -__v').lean())));
app.get('/fetchDealers/:state',safe(async(req,res)=>res.json(await Dealers.find({state:req.params.state}).sort({id:1}).select('-_id -__v').lean())));
app.get('/fetchDealer/:id',safe(async(req,res)=>{
 const dealer=await Dealers.findOne({id:req.params.id}).select('-_id -__v').lean();
 if(!dealer)return res.status(404).json({error:'Dealer not found'});res.json(dealer);
}));
app.post('/insert_review',safe(async(req,res)=>{
 const data=req.body;
 if(!await Dealers.exists({id:data.dealership}))return res.status(404).json({error:'Dealer not found'});
 if(!data.review?.trim())return res.status(400).json({error:'Review text is required'});
 const next=await mongoose.connection.collection('counters').findOneAndUpdate({_id:'reviews'},{$inc:{seq:1}},{upsert:true,returnDocument:'after'});
 const review=await Reviews.create({...data,id:next.seq});
 const result=review.toObject();delete result._id;delete result.__v;res.status(201).json(result);
}));
app.use((err,req,res,next)=>{console.error(err.message);res.status(['ValidationError','CastError'].includes(err.name)?400:500).json({error:'Unable to process the request'});});
async function start(uri){
 await mongoose.connect(uri,{dbName:'dealershipsDB'});
 if(!await Dealers.exists({}))await Dealers.insertMany(JSON.parse(fs.readFileSync(path.join(__dirname,'data/dealerships.json'))).dealerships);
 if(!await Reviews.exists({}))await Reviews.insertMany(JSON.parse(fs.readFileSync(path.join(__dirname,'data/reviews.json'))).reviews);
 const latest=await Reviews.findOne().sort({id:-1});
 await mongoose.connection.collection('counters').updateOne({_id:'reviews'},{$max:{seq:latest?.id||0}},{upsert:true});
 return app.listen(process.env.PORT||3030,'0.0.0.0',()=>console.log('Dealership API running on port '+(process.env.PORT||3030)+'; MongoDB connected'));
}
if(require.main===module)start(process.env.MONGODB_URI||'mongodb://127.0.0.1:27017').catch(err=>{console.error(err);process.exit(1);});
module.exports={app,start};
