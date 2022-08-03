package com.example.Primes;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableAsync;

@SpringBootApplication
@EnableAsync
public class PrimesApplication {

	public static void main(String[] args) {
		SpringApplication.run(PrimesApplication.class, args);
	}

}
