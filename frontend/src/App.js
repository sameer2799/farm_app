import { useState, useEffect } from 'react';
import axios from './axiosConfig';
import './App.css';

import ListToDoLists from './ListToDoLists';
import ToDoList from './ToDoList';


function App() {
  const [listSummaries, setlistSummaries] = useState(null);
  const [selectedItem, setselectedItem] = useState(null);

  useEffect(() => {
    reloadData().catch(console.error);
  }, [])

  async function reloadData() {
    const response = await axios.get('/api/lists');
    const data = await response.data;
    setlistSummaries(data);
  }

  function handleNewList(newName) {
    const updateData = async () => {
      const newListData = {
        name: newName
      };
      await axios.post('/api/lists', newListData);
      reloadData().catch(console.error);
    }
    updateData();
  }

  function handleDeleteList(id) {
    const updateData = async () => {
      await axios.delete(`/api/lists/${id}`);
      reloadData().catch(console.error);
    }
    updateData();
  }

  function handleSelectList(id) {
    console.log('Selecting item', id);
    setselectedItem(id);
  }

  function handleDeselectList() {
    setselectedItem(null);
    reloadData().catch(console.error);
  }

  if (selectedItem === null) {
    return (
      <div className="App">
        <ListToDoLists 
          listSummaries={listSummaries}
          onSelect={handleSelectList}
          onDelete={handleDeleteList}
          onNew={handleNewList}
        />
      </div>
    );
  } else {
    return (
      <div className="App">
        <ToDoList listId={selectedItem} handleBackButton={handleDeselectList}/>
      </div>
    );
}
}

export default App;
