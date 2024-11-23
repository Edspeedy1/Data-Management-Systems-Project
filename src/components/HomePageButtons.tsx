import React from "react";

export const HomePageButtons: React.FC = () => {
    const buttons = [{"text":"Create Repo", "link":"/createRepo"}, {"text":"Account Info", "link":"/accountInfo"}, {"text":"Settings", "link":"/settings"}];

    const buttonElements = buttons.map((buttonInfo) => (
        <button key={buttonInfo.text} className="m-3 pt-4 pb-4 p-2 bg-light text-white rounded-xl w-[calc(100%-40px)]" onClick={() => window.location.href = buttonInfo.link}>
            {buttonInfo.text}
        </button>
    ));

    return (
        <div className="flex flex-col items-center">
            {buttonElements}
        </div>
    );
};
