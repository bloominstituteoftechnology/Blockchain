import React,{useState, useEffect} from 'react';
import axios from 'axios';

const baseURL = `http://0.0.0.0:5000`;
function App() {
const [data, setData] = useState([]);

const FetchData = ()=>{
  axios.get(`${baseURL}/chain`).then(res=>{
    setData(res.data)
  }).catch(err => {
    return err.statusText;
  });
}

useEffect(()=>FetchData(), [])
console.log('=====',data)
  return (
    <div className="App">
      data && {
        data.chain.map(block=>{
          return (
            <div>
              {block}
            </div>
          )
        })
      }
    </div>
  );
}

export default App;
