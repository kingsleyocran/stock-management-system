"use client";
import styles from "./page.module.css";
import { useEffect, useState, useRef } from "react";
import { ACCESS_KEY, REFRESH_KEY } from "./utils/constants";
import Header from "./components/header";
import Search from "./components/search";
import ProductList from "./components/products";
import { getProducts, getProductByName, getUserDetail } from "./utils";
import { ProductModel } from "./modal";

export default function Home() {
  const [products, setProducts] = useState([]);
  const [searchText, setSearchText] = useState("");
  const searchProducts = useRef([]);
  const [userDetails, setUserDetails] = useState({});
  const [cartList, setCartList] = useState([]);
  const [showProductsFound, setShowProductsFound] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const singleProduct = useRef({});

  // all handlers here
  const handleClick = (productId) => {
    singleProduct.current = products.filter(
      (product) => product.id === productId
    );
    setShowModal((prev) => !prev);
  };

  const handleChange = (e) => {
    const value = e.target.value;
    setSearchText(value);

    if (value.length === 0) {
      // show existing products in store
      searchProducts.current = products;

      // update the existing products
      getProducts(1).then((data) => {
        searchProducts.current = data.items;
        setProducts(data.items);
      });
    } else if (searchProducts.current.length === 0) {
      setShowProductsFound(true);
      getProductByName(value).then((data) => {
        setProducts(data);
        searchProducts.current = data;
        if (data.length === 0) {
          setShowProductsFound(false);
        }
      });
    } else {
      searchProducts.current = products.filter(
        (product) =>
          JSON.stringify(product).toLowerCase().indexOf(value.toLowerCase()) >
          -1
      );
    }
  };

  // useEffects
  useEffect(() => {
    const fetchData = () => {
      getProducts(1).then((data) => {
        setProducts(data.items);
        searchProducts.current = data.items;
      });
    };

    const getUserDetailsifLoggedIn = () => {
      const token = localStorage.getItem(ACCESS_KEY);
      const refreshToken = localStorage.getItem(REFRESH_KEY);

      if (token?.length > 0 && refreshToken?.length > 0) {
        getUserDetail().then((data) => {
          if (!data?.error) {
            setUserDetails(data);
          } else {
            removeToken();
            window.location.reload();
          }
        });
      }
    };

    fetchData();
    getUserDetailsifLoggedIn();
  }, [setProducts, searchProducts, setUserDetails]);

  return (
    <>
      <Header
        singleProduct={singleProduct}
        cartList={cartList}
        setCartList={setCartList}
        userDetails={userDetails}
      />

      <Search searchText={searchText} handleChange={handleChange} />
      {showModal ? (
        <ProductModel
          product={singleProduct.current}
          setCartList={setCartList}
          isLoggedIn={Object.keys(userDetails).length > 0}
          setShowModal={setShowModal}
        />
      ) : (
        ""
      )}
      <main className={styles.main}>
        <div className={styles.grid}>
          <ProductList
            searchProducts={searchProducts}
            handleClick={handleClick}
            showProductsFound={showProductsFound}
          />
        </div>
      </main>
    </>
  );
}
