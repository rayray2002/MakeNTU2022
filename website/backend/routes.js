import express from 'express'
import { StatModel } from './model';

export default()=>{
    const router = express.Router();

    router.get('/data',async(_,res)=>{
        //const {device,stat} = req.query;
        //console.log(device,stat);
        let data;
        data = await StatModel.find({});
        console.log(data)
        res.json(data).end();
    })
    return router;
};