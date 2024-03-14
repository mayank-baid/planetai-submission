import React, { useState, useEffect } from 'react';
import './Header.css';
import logo from './assets/logo.svg';
import pdfLogo from './assets/pdflogo.svg';
import add from './assets/add.svg';

const Header = ({ pdfName, onPdfUpload }) => {
    const [truncatedPdfName, setTruncatedPdfName] = useState(pdfName);

    useEffect(() => {
        const handleResize = () => {
            if (window.innerWidth < 768) {
                setTruncatedPdfName(truncateFileName(pdfName));
            } else {
                setTruncatedPdfName(pdfName);
            }
        };

        window.addEventListener('resize', handleResize);

        return () => {
            window.removeEventListener('resize', handleResize);
        };
    }, [pdfName]);

    const truncateFileName = (name) => {
        return name.length > 10 ? name.substring(0, 7) + '...' : name;
    };

    return (
        <header>
            <div className="logo">
                <img src={logo} alt="Logo" />
            </div>
            <div className="upload-btn">
                {pdfName && (
                    <span className='pdf-details'>
                        <img src={pdfLogo} alt="" />
                        {truncatedPdfName || pdfName}
                    </span>
                )}
                <input
                    type="file"
                    id="pdfInput"
                    onChange={onPdfUpload}
                    accept=".pdf"
                    style={{ display: 'none' }}
                />
                <label className='pdf-input' htmlFor="pdfInput">
                    <img className='pdf-input-add-btn' src={add} alt="" />
                    <p className='pdf-input-text'>Upload PDF</p>
                </label>
            </div>
        </header>
    );
};

export default Header;
