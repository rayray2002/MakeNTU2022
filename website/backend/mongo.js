import mongoose from "mongoose";

mongoose.connect(process.env.MONGO_URL,{
    useNewUrlParser: true,
    useUnifiedTopology: true,
}).then((res) => console.log("mongodb connected"));