import './ListsToDoLists.css';
import { useRef } from 'react';
import { BiSolidTrash } from 'react-icons/bi';

function ListToDoLists({ listSummaries, onSelect, onDelete, onNew }) {
    const labelRef = useRef();
    
    if (listSummaries === null) {
        return <div className='ListToDoLists loading'>Loading To-Do lists...</div>;
    } else if (listSummaries.length === 0) {
        return (
            <div className='ListToDoLists'>
                <div className='box'>
                    <label>
                        New To-Do List:&nbsp;
                        <input id={labelRef} type='text' placeholder='New list name' />
                    </label>
                    <button
                        onClick={() => onNew(document.getElementById(labelRef).value)}
                    >
                        New
                    </button>
                </div>
                <p>No To-Do lists found.</p>
            </div>
        );
    }
        return (
            <div className="ListToDoLists">
                <h1>All To-Do Lists</h1>
                <div className='box'>
                    <label>
                        New To-Do List:&nbsp;
                        <input id={labelRef} type='text' placeholder='New list name' />
                    </label>
                    <button onClick={() => onNew(document.getElementById(labelRef).value)}>
                        New list
                    </button>
                </div>
                {listSummaries.map((summary) => {
                    return (
                        <div key={summary.id} className="summary" onClick={() => onSelect(summary.id)}>
                            <span className='name'>{summary.name}</span>
                            <span className='count'>({summary.item_count} items)</span>
                            <span className='flex'></span>
                            <span className='trash' onClick={(evt) => {
                                evt.stopPropagation();
                                onDelete(summary.id);
                            }}>
                                <BiSolidTrash />
                            </span>
                        </div>
                    );
                })}
            </div>
        );
}

export default ListToDoLists;