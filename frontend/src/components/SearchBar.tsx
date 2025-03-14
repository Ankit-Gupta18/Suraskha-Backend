import React, { useState } from "react";

interface SearchBarProps {
  users: { id: number; name: string; avatar: string }[];
  onSearchResults: (results: { id: number; name: string; avatar: string }[]) => void;
}

const SearchBar: React.FC<SearchBarProps> = ({ users, onSearchResults }) => {
  const [query, setQuery] = useState("");

  const handleSearch = (e: React.ChangeEvent<HTMLInputElement>) => {
    const searchTerm = e.target.value.toLowerCase();
    setQuery(searchTerm);

    // Filter users based on name
    const filteredUsers = users.filter((user) =>
      user.name.toLowerCase().includes(searchTerm)
    );

    onSearchResults(filteredUsers);
  };

  return (
    <input
      type="text"
      className="search-bar"
      placeholder="Search users..."
      value={query}
      onChange={handleSearch}
    />
  );
};

export default SearchBar;
