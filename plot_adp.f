C author: By Student
c
      call writeset
      stop
      end
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c write out plt file.                                             c
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
      subroutine writeset
      implicit real*8 (a-h,o-z)
      implicit integer*8 (i-m)
      character*80 outfile,outelem
      common /pass1/ re(16),fe(16),rhoe(16),alpha(16),
     *   beta(16),beta1(16),A(16),B(16),cai(16),ramda(16),
     *   ramda1(16),Fi0(16),Fi1(16),Fi2(16),Fi3(16),
     *   Fm0(16),Fm1(16),Fm2(16),Fm3(16),Fm4(16),
     *   fnn(16),Fn(16),rhoin(16),rhoout(16),rhol(16),
     *   rhoh(16),rhos(16)
      common /pass2/ amass(16),Fr(50000,16),rhor(50000,16),
     *   rphi(50000,16,16),blat(16),drho,dr,rc,outfile,outelem
      common /pass3/ ielement(16),ntypes,nrho,nr
      real u(50000,16,16)
      real w(50000,16,16)
      character*80 dump
      character*80 struc
c      struc='fcc'
c      outfile = outfile(1:index(outfile,' ')-1)//'_Zhou04.eam.alloy'
c      open(unit=1,file=outfile)
      open(unit=1,file='Xx.adp')
      open(unit=2,file='F.plt')
      open(unit=3,file='rho.plt')
      open(unit=4,file='rphi.plt')
      open(unit=7,file='u.plt')
      open(unit=8,file='w.plt')
      read(1,*) dump 
c      write(6,*) dump
c      write(1,*) '# DATE: 2018-03-30 ',
c     *   'CONTRIBUTOR: Xiaowang Zhou xzhou@sandia.gov and ',
c     *   'Lucas Hale lucas.hale@nist.gov ',
c     *   'CITATION: X. W. Zhou, R. A. Johnson, ',
c     *   'H. N. G. Wadley, Phys. Rev. B, 69, 144113(2004)'
      read(1,*) dump
c      write(6,*) dump
c      write(1,*) '# Generated from Zhou04_create_v2.f'
      read(1,*) dump
c      write(6,*) dump
c      write(1,*) '# Fixes precision issues with older version'
      read(1,*) ntypes,outelem
8     format(i5,a24)
c      write(1,8)ntypes,outelem
c8     format(i5,' ',a24)
      read(1,*) nrho,drho,nr,dr,rc
c      write(1,9)nrho,drho,nr,dr,rc
9     format(i5,e24.16,i5,2e24.16)
      do 10 i=1,ntypes
        read(1,*) ielement(i),amass(i),blat(i) 
c        write(1,11)ielement(i),amass(i),blat(i),struc
        read(1,*) (Fr(j,i),j=1,nrho)
c        write(1,12)(Fr(j,i),j=1,nrho)
        read(1,*) (rhor(j,i),j=1,nr)
c        write(1,12)(rhor(j,i),j=1,nr)
        write(2,*) "# atom ",i
        do 15 j=1,nrho
          write(2,*) (j-1)*drho,Fr(j,i)
15      continue
        write(2,*) " "
        write(3,*) "# atom ",i
        do 16 j=1,nr
          write(3,*) (j-1)*dr,rhor(j,i)
16      continue
        write(3,*) " "
10    continue
11    format(i5,2g15.5,a8)
12    format(5e24.16)
      do 13 i1=1,ntypes
        do 13 i2=1,i1
          read(1,*) (rphi(i,i1,i2),i=1,nr)
c          write(1,12)(z2r(i,i1,i2),i=1,nr)
          write(4,*) "# atom,atom ",i1,",",i2
          do 20 j=1,nr
            write(4,*) (j-1)*dr,rphi(j,i1,i2)
20        continue
          write(4,*) " "
13    continue
14    format(f15.10,' ',f15.10)
      do 31 i1=1,ntypes
        do 31 i2=1,i1
          read(1,*) (u(i,i1,i2),i=1,nr)
          write(7,*) "# atom,atom ",i1,",",i2
          do 32 j=1,nr
            write(7,*) (j-1)*dr,u(j,i1,i2)
32        continue
          write(7,*) " "
31    continue
      do 41 i1=1,ntypes
        do 41 i2=1,i1
          read(1,*) (w(i,i1,i2),i=1,nr)
          write(8,*) "# atom,atom ",i1,",",i2
          do 42 j=1,nr
            write(8,*) (j-1)*dr,w(j,i1,i2)
42        continue
          write(8,*) " "
41    continue
      close(1)
      close(2)
      close(3)
      close(4)
      return
      end
