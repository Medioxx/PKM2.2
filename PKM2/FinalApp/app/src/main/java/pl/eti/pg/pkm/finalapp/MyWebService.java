package pl.eti.pg.pkm.finalapp;


import java.util.Map;

import retrofit2.Call;
import retrofit2.http.Body;
import retrofit2.http.GET;
import retrofit2.http.POST;

/**
 * Created by EO NETWORKS on 13.12.2017.
 */
//interfejs definiujący metody używane do komunikacji z restapi
public interface MyWebService {

    //ustawianie algorytmów
    @POST("/logs/set_algorithms")
    Call<Map<String, String>> postAlgorithms(@Body Map<String, String> algorithms);

    //sterowanie szybkością pociągu
    @POST("/train/set_speed")
    Call<Map<String, String>> postControl(@Body Map<String, String> control);

    //wysyłanie informacji o sieci neuronowej
    @GET("/neural/set_frame")
    Call<Void> postNeural();


}
