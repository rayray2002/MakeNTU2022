import { StatModel } from "./model";

const sample = [
    {
        stat:[1,2,3,4,5]
    }
]

const dataInit = async()=>{
    await StatModel.deleteMany({});
    await StatModel.insertMany(sample);
}

export {dataInit};
