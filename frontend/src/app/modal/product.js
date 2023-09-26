"use client";
import Image from "next/image";
import styles from "../page.module.css";
import modalStyles from "../modal.module.css";
import { useState, useRef } from "react";
import { faCloudUpload } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Loading } from "./utils";
import { addProduct, addProductImage } from "../utils";

export function AddProductModel({ onShow }) {
  const initialState = {
    name: "",
    description: "",
    category: "",
    quantity: "",
    price: "",
  };

  const previewElement = useRef();
  const [productInfo, setProductInfo] = useState(initialState);
  const image = useRef(null);
  const [showLoading, setShowLoading] = useState(false);
  const [showError, setShowError] = useState("");
  const [done, setDone] = useState("");
  const [sentProduct, setSentProduct] = useState(false);

  const handleClose = (e) => {
    if (sentProduct) {
      onShow();
      windows.location.reload();
    }
    onShow();
  };
  const handleSubmit = (e) => {
    e.preventDefault();
    setShowError("");
    setDone("");
    setShowLoading((prev) => !prev);
    addProduct(productInfo).then((data) => {
      if (!data?.error) {
        // add image to product
        if (image.current) {
          addProductImage(data.id, image.current).then((data) => {
            previewElement.current.src = "./store.svg";
          });
          setSentProduct((prev) => !prev);
          setDone("Product Added to Store");
        }
      } else {
        setShowError(data?.error);
      }
      setProductInfo(initialState);
      setShowLoading((prev) => !prev);
    });
  };

  const handleProductChange = (e) => {
    setProductInfo({ ...productInfo, [e.target.name]: e.target.value });
  };

  const handleChangeImage = (e) => {
    if (e.target.files.length > 0) {
      const imageUploaded = e.target.files[0];
      const src = URL.createObjectURL(imageUploaded);
      previewElement.current.src = src;
      previewElement.current.style.display = "block";
      image.current = imageUploaded;
    }
  };

  return (
    <>
      <div className={styles.modal}>
        <div className={styles.modalContent}>
          <span className={styles.close} onClick={handleClose}>
            &times;
          </span>

          {showError.length > 0 ? (
            <p className={styles.errorMsg}>{showError}</p>
          ) : (
            ""
          )}

          {done.length > 0 ? <h1>{done}</h1> : ""}

          <div className={styles.addProductContainer}>
            <div className={modalStyles.formInput}>
              <div className={modalStyles.preview}>
                <Image
                  src="./store.svg"
                  alt="product"
                  width={200}
                  height={250}
                  ref={previewElement}
                />
              </div>
              <label htmlFor="upload-file">
                <FontAwesomeIcon icon={faCloudUpload} /> &nbsp;Upload Product
                Image
              </label>
              <input
                type="file"
                id="upload-file"
                accept="image/*,.png,.jpg"
                onChange={handleChangeImage}
                disabled={showLoading}
              />
            </div>

            {showLoading ? (
              <div className={`${styles.center} ${styles.done}`}>
                <Loading />
              </div>
            ) : (
              ""
            )}

            <form action="" onSubmit={handleSubmit}>
              <div className={styles.addProductInputDetails}>
                <label htmlFor="name">Product Name</label>
                <input
                  id="name"
                  type="text"
                  name="name"
                  disabled={showLoading}
                  required
                  onChange={handleProductChange}
                  value={productInfo.name}
                />
                <label htmlFor="description">Product Description</label>
                <textarea
                  id="description"
                  name="description"
                  disabled={showLoading}
                  required
                  value={productInfo.description}
                  onChange={handleProductChange}
                />
                <label htmlFor="category">Product Category</label>
                <input
                  id="category"
                  type="text"
                  name="category"
                  disabled={showLoading}
                  required
                  onChange={handleProductChange}
                  value={productInfo.category}
                />
                <label htmlFor="quantity">Product Quantity</label>
                <input
                  id="quantity"
                  type="number"
                  name="quantity"
                  disabled={showLoading}
                  min={1}
                  required
                  value={productInfo.quantity}
                  onChange={handleProductChange}
                />
                <label htmlFor="price">Product Price</label>
                <input
                  id="price"
                  type="number"
                  name="price"
                  min={1}
                  disabled={showLoading}
                  required
                  value={productInfo.price}
                  onChange={handleProductChange}
                />
                <button type="submit" disabled={showLoading}>
                  Add Product
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </>
  );
}
