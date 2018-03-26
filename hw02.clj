;; Author: Daniel R. Schlegel
;; Simulation of the Monty Hall Problem.
;; Created 12/4/2015

(ns monty-hall-simulation.core)

(def simulation-cycles 1000000)

;; Create a 3-tuple with 1 in a random location.
(defn create-doors []
  (assoc [0 0 0] (rand-int 3) 1))
  
(defn choose-door []
  (rand-int 3))

;; Returns the index of the revealed goat.
(defn reveal-goat [doors selected-index]
  (let [unselected-idxes (remove #{selected-index} (range 3))]
	  (cond 
	    ;; Selected a car -> randomly pick one of the other two indices to reveal.
	    (= (nth doors selected-index) 1)
      (nth unselected-idxes (rand-int 2))
	    ;; Selected a goat -> reveal the other goat.
	    :default
	    (if (= (nth doors (first unselected-idxes)) 0)
       (first unselected-idxes)
       (second unselected-idxes)))))

(defn monty-hall [change-guess?]
  (let [doors (create-doors)
        choice-idx (choose-door)
        revealed-goat-idx (reveal-goat doors choice-idx)
        choice-idx (if change-guess?
                     (first (remove #{choice-idx revealed-goat-idx} (range 3)))
                     choice-idx)]
    ;; Return what's behind the chosen door.
    (nth doors choice-idx)))

(defn simulate [change-guess?]
  (if change-guess?
    (println "Monty Hall Simulator - Changing Guess on Reveal -" simulation-cycles "iterations")
    (println "Monty Hall Simulator - Not Changing Guess on Reveal -" simulation-cycles "iterations"))
  
  (loop [n simulation-cycles
         results []]
    (if (> n 0)
      (recur (dec n)
             (conj results (monty-hall change-guess?)))
      (float (/ (count (filter #{1} results)) (count results))))))
