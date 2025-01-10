import React, { useState } from 'react';
import './IconWithDropdown.css'; // Include the CSS styles

const IconWithDropdown = ({
  iconSrc,
  altText,
  isSelected,
  onSelect,
}) => {
  return (
    <div className="icon-container" onClick={(e) => e.stopPropagation()}>
      <a
        href="#"
        className={`circle-icon ${isSelected ? 'selected' : ''}`}
        onClick={(e) => {
          e.preventDefault();
          onSelect();
        }}
      >
        <img src={iconSrc} alt={altText} />
      </a>
    </div>
  );
};

const IconList = ({ onIconSelect }) => {
  const [selectedIconIndex, setSelectedIconIndex] = useState(0);

  const icons = [
    {
      src: '/images/nintendo_icon.png',
      alt: 'Nintendo Icon',
      consoles: [
        { value: 'nes', name: 'Nintendo Entertainment System (NES)' },
        { value: 'super-nintendo', name: 'Super Nintendo Entertainment System (NES)' },
        { value: 'nintendo-64', name: 'Nintendo 64' },
        { value: 'gamecube', name: 'Gamecube' },
        { value: 'wii', name: 'Wii' },
        { value: 'wii-u', name: 'Wii U' },
        { value: 'nintendo-switch', name: 'Switch' },
        { value: 'gameboy', name: 'Gameboy' },
        { value: 'gameboy-color', name: 'Gameboy Color' },
        { value: 'gameboy-advance', name: 'Gameboy Advance' },
        { value: 'nintendo-ds', name: 'DS' },
        { value: 'nintendo-3ds', name: '3DS' },
        { value: 'virtual-boy', name: 'Virtual Boy' },
        { value: 'game-&-watch', name: 'Game & Watch' }
      ],
    },
    {
      src: '/images/playstation_icon.png',
      alt: 'PlayStation Icon',
      consoles: [
        { value: 'playstation', name: 'PlayStation 1' },
        { value: 'playstation-2', name: 'PlayStation 2' },
        { value: 'playstation-3', name: 'PlayStation 3' },
        { value: 'playstation-4', name: 'PlayStation 4' },
        { value: 'playstation-5', name: 'PlayStation 5' },
        { value: 'psp', name: 'PlayStation Portable' },
        { value: 'playstation-vita', name: 'PlayStation Vita' }
      ],
    },
    {
      src: '/images/xbox_icon.png',
      alt: 'Xbox Icon',
      consoles: [
        { value: 'xbox', name: 'Original Xbox' },
        { value: 'xbox-360', name: 'Xbox 360' },
        { value: 'xbox-one', name: 'Xbox One' },
        { value: 'xbox-series-x', name: 'Xbox Series X' },
      ],
    },
    {
      src: '/images/sega_icon.png',
      alt: 'Sega Icon',
      consoles: [
        { value: 'nes', name: 'NES' },
        { value: 'super-nintendo', name: 'Super Nintendo' }
      ],
    },
    {
      src: '/images/atari_icon.png',
      alt: 'Atari Icon',
      consoles: [
        { value: 'nes', name: 'NES' },
        { value: 'super-nintendo', name: 'Super Nintendo' }
      ],
    },
    {
      src: '/images/other_icon.png',
      alt: 'Other Icon',
      consoles: [
        { value: 'nes', name: 'NES' },
        { value: 'super-nintendo', name: 'Super Nintendo' }
      ],
    },
  ];

  const handleSelectIcon = (index) => {
    setSelectedIconIndex(index);
    onIconSelect(icons[index].consoles);
  };

  return (
    <div className="icon-list">
      {icons.map((icon, index) => (
        <IconWithDropdown
          key={index}
          iconSrc={icon.src}
          altText={icon.alt}
          isSelected={selectedIconIndex === index}
          onSelect={() => handleSelectIcon(index)}
        />
      ))}
    </div>
  );
};

const App = () => {
  const [selectedConsole, setSelectedConsole] = useState('nes');
  const [consoleOptions, setConsoleOptions] = useState([
    { value: 'nes', name: 'NES' },
    { value: 'super-nintendo', name: 'Super Nintendo' },
  ]);

  const handleSelectedConsole = (e) => {
    setSelectedConsole(e.target.value);
  };

  const handleIconSelect = (consoles) => {
    setConsoleOptions(consoles);
    setSelectedConsole(consoles[0].value);
  };

  return (
    <div>
      <IconList onIconSelect={handleIconSelect} />
      <div className="form-item">
        <label className="label">
          <select
            name="console"
            value={selectedConsole}
            onChange={handleSelectedConsole}
            className="select-input"
          >
            {consoleOptions.map((console, index) => (
              <option key={index} value={console.value}>
                {console.name}
              </option>
            ))}
          </select>
        </label>
      </div>
    </div>
  );
};

export default App;
