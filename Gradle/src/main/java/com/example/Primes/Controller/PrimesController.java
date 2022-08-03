package com.example.Primes.Controller;

import com.example.Primes.Service.PrimesService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.concurrent.CompletableFuture;

@RestController
public class PrimesController {

    @Autowired
    private PrimesService concurrency;

    @GetMapping("/primes")
    public CompletableFuture<String> getPrime(@RequestParam("start") int start, @RequestParam("end") int end){

        return concurrency.Prime(start, end);
    }
}
