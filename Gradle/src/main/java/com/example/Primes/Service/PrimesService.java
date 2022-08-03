package com.example.Primes.Service;

import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Service;

import java.util.concurrent.CompletableFuture;

@Service
public class PrimesService {

    private boolean isPrime(int num){

        if(num>1) {
            double s = Math.sqrt(num);
            for (int j = 2; j <= s; j++)
                if (num % j == 0) {
                    return false;
                }
        }else return false;

        return true;
    }

    @Async
    public CompletableFuture<String> Prime(int start, int end){
        int sum = 0;
        System.out.println("OK " + Thread.currentThread().getName() + " " + start + " " + end);

        for (int i = start; i <= end; i++)
            if(isPrime(i)) sum++;

        String res = String.valueOf(sum);

        return CompletableFuture.completedFuture(res);
    }
}
