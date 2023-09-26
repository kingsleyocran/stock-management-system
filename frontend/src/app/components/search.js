import styles from "../page.module.css";
export default function Search({ handleChange, searchText }) {
  return (
    <>
      <div className={styles.searchContainer}>
        <input
          type={"search"}
          placeholder={"Search Product"}
          className={styles.search}
          onChange={handleChange}
          value={searchText}
        />
      </div>
    </>
  );
}
