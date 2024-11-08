import React, { useState } from 'react';

export const LoginInputs: React.FC = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [isActive, setIsActive] = useState(false);

    // Use effect to track changes in username and password and update the button state immediately
    React.useEffect(() => {
        
        if (username.trim() && password.trim()) {
            setIsActive(true);
        } else {
            setIsActive(false);
        }
    }, [username, password]); // Effect runs when username or password changes

    // Handlers for input changes
    const handleUsernameChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setUsername(e.target.value);
    };

    const handlePasswordChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setPassword(e.target.value);
    };

    function handleSubmit() {
        if (!username || !password) {
            return;
        }
        fetch('/login', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ username, password }) }).then(
        response => response.json()).then(
            data => {
                if (data.success) {
                    console.log("redirecting...");
                    window.location.href = '/home';
                }
    })};

    return (
        <div className="h-[30vh] lg:w-[20vw] flex flex-col justify-center items-center">
        <input
            type="text"
            name="username"
            id="username"
            placeholder="username"
            onChange={handleUsernameChange}
            className="p-2 border-2 border-black mt-4 mb-4"
        />
        <input
            type="password"
            name="password"
            id="password"
            placeholder="password"
            onChange={handlePasswordChange}
            className="p-2 border-2 border-black mt-4 mb-4"
            onKeyDown={(e) => {
                console.log(e.key);
                if (e.key === 'Enter') {
                    handleSubmit();
                }
            }}
        />
        <button className={` ${isActive ? "p-2 border-2 border-black mt-4 mb-4 bg-dark text-white" : "p-2 border-2 border-dark mt-4 mb-4 bg-light text-black"}`}
            onClick={handleSubmit}
            disabled={!isActive} 
        >Submit</button>
        </div>

    )
}