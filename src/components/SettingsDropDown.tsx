import React, { useState } from "react";
import clsx from "clsx";
import { ToggleBox } from "./ToggleBox";


export const SettingsDropDown: React.FC = () => {
    const [isOpen, setIsOpen] = useState(false);

    return (
        <div className="h-[30%]">
            <div
                className={clsx("h-full w-full flex flex-col justify-center transition-all duration-300 items-center", isOpen ? "-translate-y-12" : "translate-y-0")}
            >
                <button className="flex items-center cursor-pointer"
                onClick={() => setIsOpen(!isOpen)}>
                    <img src="../content/gear-svgrepo-com.svg" className="h-8" alt="Settings Icon" />
                    <p className="ml-2">Settings</p>
                </button>
                <div className={clsx("duration-300 w-full", isOpen ? "opacity-100 cursor-pointer translate-y-0" : "opacity-0 cursor-default translate-x-[1000px]")}>
                    <ToggleBox api="repoPublic">Is Public</ToggleBox>
                    {/* <ToggleBox>Public</ToggleBox>
                    <ToggleBox>Public</ToggleBox>
                    <ToggleBox>Public</ToggleBox> */}
                </div>
            </div>
        </div>
    );
};