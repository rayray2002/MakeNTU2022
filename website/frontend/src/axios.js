import axios from 'axios'

const instance = axios.create({baseURL: 'http://localhost:5000/api'})

const getalldata = async() =>{
    try{
        //console.log(device,stat);
        console.log('l');
        const {data} = await instance.get('/data',{});
        console.log(data);
        return data;
    }catch(error){
        console.log(error);
    }
}
export {getalldata};