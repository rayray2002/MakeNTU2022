import express from 'express'
import cors from 'cors'
//import Router from './routes/index'
import mongoose from "mongoose"; 
import 'dotenv/config'
import routes from './routes';
import { dataInit } from './testdata';

const app = express()
app.use(express.json())
app.use(cors())
 
app.use("/api", routes);

const port = process.env.PORT || 5000

mongoose.connect(process.env.MONGO_URL,{
    useNewUrlParser: true,
    useUnifiedTopology: true,
})
const db = mongoose.connection;
db.once("open",()=>{
    console.log('mongoDB connected successfully')
    dataInit();
})


app.listen(port,()=>{
    console.log(`Server is up on port ${port}.`)
})
      