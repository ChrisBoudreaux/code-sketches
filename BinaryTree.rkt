#lang scheme

(define atom?
  (lambda (a)
    (cond
      ((number? a) #t)
      ((symbol? a) #t)
      (else #f))))

; The following lines define a set of Binary Trees and non-Binary Trees for the algorithms to test
; A Binary Tree is represented as follows, where LEFTCHILD and RIGHTCHILD are Binary Trees with values
; of the same type as ROOT (ROOT (LEFTCHILD) (RIGHTCHILD))
(define TestTree1 '(1 (2 (4 ()())(5()()))(3 (6()())(7()() ))))

(define TestTree2 '(1 (2 (4 ()()) (5 () ())) ()))

(define NotATree1 '(1 2 3))

(define NotATree2 '(1 (2 () ()) (3 () ()) (4 () ())))

(define TestTree3 '(1 (2 (4 ()()) () ) ()))

; This function returns a function that checks if t is a binary tree, where each root is tested
; against the function specified by the function type?
(define binaryTree?
  (lambda (type?)
    (lambda (t)
      (cond
        ((atom? t) #f) ;established as a list
        ((or (atom? (leftTree t)) (atom? (rightTree t))) #f) ;established both children are lists
        ((binaryLeaf? t) #t) ;t is a leaf node
        (else (and (type? (rootTree t)) 
                   (and (null? (cdr (cdr (cdr t)))) 
                        (and ((binaryTree? type?)(leftTree t)) 
                             ((binaryTree? type?)(rightTree t))))))))))

(define binaryTreeOfAtoms? (binaryTree? atom?) )

(define rootTree
  (lambda (t)
    (car t)))

(define binaryLeaf?
  (lambda (binaryNode)
    (and (null? (leftTree binaryNode)) (null? (rightTree binaryNode)))))

(define leftTree
  (lambda (t)
    (car (cdr t))))

(define rightTree
  (lambda (t)
    (car (cdr (cdr t)))))

(define createBinaryLeaf
  (lambda (root)
    (cons root (cons '() '(())))))
    
(define budTrees
  (lambda (root leftTree rightTree)
    (cons root (cons (cons leftTree '()) (cons rightTree '() )))))

(define inOrder
  (lambda (visitFunct)
    (lambda (tree)
      (inOrder (leftTree tree))
      (visitFunct (root tree))
      


