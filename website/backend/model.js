import mongoose from "mongoose";

const {Schema} = mongoose

const StatSchema = new Schema({
    stat:{type:[Number],required:true}
})

const StatModel = mongoose.model("Stat",StatSchema)

export{StatModel};