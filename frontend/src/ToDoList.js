import './ToDoList.css';
import { useRef, useState, useEffect } from 'react';
import { BiSolidTrash } from 'react-icons/bi';
import axios from './axiosConfig';

function ToDoList({ listId, handleBackButton }) {
    const labelRef = useRef();
    const [listData, setListData] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            const response = await axios.get(`/api/lists/${listId}`);
            const newData = await response.data;
            setListData(newData);
        };
        fetchData().catch(console.error);
    }, [listId]);

    function handleCreateItem(label) {
        const updateData = async () => {
            const response = await axios.post(`/api/lists/${listData.id}/items`, {label: label,});
            const newData = await response.data;
            setListData(newData);
        };
        updateData().catch(console.error);
    }

    function handleDeleteItem(id) {
        const updateData = async () => {
            const response = await axios.delete(`/api/lists/${listData.id}/items/${id}`);
            const newData = await response.data;
            setListData(newData);
        };
        updateData().catch(console.error);
    }

    function handleCheckToggle(id, newState) {
        const updateData = async () => {
            const response = await axios.patch(`/api/lists/${listData.id}/checked_state`, {item_id: id, checked: newState});
            const newData = await response.data;
            setListData(newData);
        };
        updateData().catch(console.error);
    }

    if (listData === null) {
        return (
            <div className='ToDoList'>
                <button className='back' onClick={handleBackButton}>
                    Back
                </button>
                Loading...
            </div>
        );
    }
    return (
        <div className='ToDoList'>
            <button className='back' onClick={handleBackButton}>
                Back
            </button>
            <h1>List: {listData.name}</h1>
            <div className='box'>
                <label>
                    New To-Do List:&nbsp;
                    <input id={labelRef} type='text' placeholder='New list name' />
                </label>
                <button
                    onClick={() => handleCreateItem(document.getElementById(labelRef).value)}
                >
                    New item
                </button>
            </div>
            {listData.items.length > 0 ? (
                listData.items.map((item) => {
                    return (
                        <div key={item.id} className={item.checked ? "item checked" : "item"} onClick={() => handleCheckToggle(item.id, !item.checked)}>
                            <span>{item.checked ? '✓' : ''}</span>
                            <span className='label'>{item.label}</span>
                            <span className='flex'></span>
                            <span className='trash' onClick={(e) => {
                                e.stopPropagation();
                                handleDeleteItem(item.id)}}
                            >
                                <BiSolidTrash />
                            </span>
                        </div>
                    );
                })
            ) : (
                <div className='box'>No items found.</div>
            )}
        </div>
    );
};

export default ToDoList;