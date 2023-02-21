import React, { useState, useEffect, useContext } from "react";
import { Link, useParams } from "react-router-dom";
import Swal from "sweetalert2";
import { Context } from "../store/appContext";
import { Navigate, useNavigate } from "react-router-dom";
import PropTypes from "prop-types";
import "../../styles/home.css";
import ReactWhatsapp from "react-whatsapp";
import { PayPalScriptProvider, PayPalButtons } from "@paypal/react-paypal-js";

export const OneRefugio = () => {
  const { store, actions } = useContext(Context);
  const navigate = useNavigate();
  const params = useParams(); //

  //Obtengo la mascota
  useEffect(() => {
    actions.getOneRefugio(params.id);
    actions.getPetsUser(params.id);
    window.scrollTo(0, 0);
  }, []);

  return (
    <div className="container-fluid">
      <div className="jumbotron  m-3">
        <div className="rounded border border-primary">
          <div className="row g-0">
            <div className="container w-75 mx-auto my-3">
              <div className="border-bottom border-primary">
                <h1 className="text-center pet-information">
                  Información del Refugio
                </h1>
              </div>
              <form>
                <div className="form-group row d-flex">
                  <div className="row">
                    <a
                      className="d-flex justify-content-center"
                      href={store.oneRefugio.url}
                    >
                      <img className="onePet" src={store.oneRefugio.url} />
                    </a>
                  </div>
                  <div className="d-flex justify-content-center">
                    <div className="col-md-6 mb-3">
                      <label className="form-label">Refugio:</label>
                      <input
                        type=""
                        className="form-control"
                        value={store.oneRefugio.empresa}
                        id="empresa"
                        readOnly
                      />
                    </div>
                  </div>
                </div>

                <div className="form-group row">
                  <h1 className="text-center border-bottom border-primary h1"></h1>
                </div>
                {store.petsUser != null ? (
                  <div className="row g-0 scrollablePerfil ">
                    <div className="col-md-12 ">
                      <div className="d-flex">
                        {store.petsUser.map((item, id) => (
                          <div className="btn m-3 ms-0 rounded " key={id}>
                            <div
                              className="card listPerfil border-primary "
                              style={{ width: "10rem", height: "10rem" }}
                            >
                              <Link
                                style={{ textDecoration: "none" }}
                                to={"/mascota/" + item.id}
                              >
                                <div className="border-bottom border-primary">
                                  <img
                                    src={item.url}
                                    className="card-img-top"
                                    alt="..."
                                  />
                                </div>
                              </Link>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                ) : null}
                <div className="d-flex justify-content-center pe-4 my-2">
                  <ReactWhatsapp
                    className="btn btn-lg btn-success"
                    number={"+598" + store.oneRefugio.contacto}
                    message="Buenas! me contacto contigo para mas información acerca de una mascota que publicaste en FindPets!"
                    onClick={(e) => e.preventDefault()}
                  >
                    Contactar <i className="fab fa-whatsapp mx-1"></i>
                  </ReactWhatsapp>
                </div>
                {store.oneRefugio.paypal_url == null ? (
                  <div className="d-flex justify-content-center pe-4 my-2">
                    <PayPalScriptProvider
                      options={{ "client-id": store.oneRefugio.paypal_url }}
                    >
                      <PayPalButtons />
                    </PayPalScriptProvider>
                  </div>
                ) : null}
                {/*  */}
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
