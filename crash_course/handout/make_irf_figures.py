import numpy as np, matplotlib, os
matplotlib.use("Agg"); import matplotlib.pyplot as plt
NAVY="#0f2355"; RUST="#b85c00"
alpha,beta,phi,sig=0.667,0.984,0.979,0.0072
def solve(delta):
    r=1/beta-(1-delta); k=0.20*((1-alpha)/r)**(1/alpha)
    y=k**(1-alpha)*0.20**alpha; i=delta*k; c=y-i; w=alpha*y/0.20
    s_i=i/y; s_c=c/y; Delta=1-alpha*(1-0.20)
    n_y=1/Delta; n_k=(1-alpha)/Delta; n_c=-alpha*(1-0.20)/Delta
    g=r/(1-alpha); br=beta*r
    A=np.array([[1,0,0],[0,1,0],[-br*(n_k-1),-br*n_y,1-br*n_c]],float)
    B=np.array([[(1-delta)+g*n_k,g*n_y,g*(n_c-s_c)],[0,phi,0],[0,0,1]],float)
    F=np.linalg.solve(A,B); wv,P=np.linalg.eig(F); Q=np.linalg.inv(P); uns=np.abs(wv)>1
    H=np.real(-np.linalg.solve(Q[np.ix_(uns,[2])],Q[np.ix_(uns,[0,1])]))
    M=np.real(F[0:2,0:2]+F[0:2,2:3]@H)
    ss=dict(y=y,c=c,i=i,k=k,h=0.20,r=r,w=w,a=1.0)
    return n_y,n_k,n_c,s_c,s_i,H,M,ss
def irf(delta,T=40,levels=True):
    n_y,n_k,n_c,s_c,s_i,H,M,ss=solve(delta)
    s=np.array([0.0,sig]); out={v:[] for v in ['y','c','i','k','h','r','w','a']}
    for t in range(T):
        kk,aa=s; cc=float(np.ravel(H@s)[0])
        yy=n_y*aa+n_k*kk+n_c*cc; hh=(1-0.20)*(yy-cc); rr=yy-kk; ww=yy-hh; ii=(yy-s_c*cc)/s_i
        d=dict(y=yy,c=cc,i=ii,k=kk,h=hh,r=rr,w=ww,a=aa)
        for v in out: out[v].append(d[v]*(ss[v] if levels else 1.0))
        s=M@s
    return {v:np.array(x) for v,x in out.items()}
labs={'y':'Producto $y$','c':'Consumo $c$','i':'Inversión $i$','k':'Capital $k$',
      'h':'Horas $h$','r':'Retorno $r$','w':'Salario $w$','a':'PTF $a$'}
b=irf(0.025)
fig,ax=plt.subplots(2,4,figsize=(11,5.2))
for j,v in enumerate(['y','c','i','k','h','r','w','a']):
    a_=ax[j//4,j%4]; a_.plot(range(len(b[v])),b[v],color=NAVY,lw=1.8)
    a_.axhline(0,color='0.6',lw=.7,ls=':'); a_.set_title(labs[v],fontsize=10)
    a_.grid(alpha=.25); a_.tick_params(labelsize=8); a_.ticklabel_format(axis='y',style='sci',scilimits=(-2,2))
fig.suptitle('IRFs a un choque de productividad de 1 desv. est. ($\\delta=0.025$), desviaciones del EE',fontsize=12)
fig.tight_layout(rect=[0,0,1,0.96]); fig.savefig("handout/assets/irf_base.pdf"); plt.close(fig)
h1=irf(1.0)['h']; h2=irf(0.025)['h']
fig2,ax2=plt.subplots(figsize=(6.6,3.4))
ax2.plot(range(len(h2)),h2,color=NAVY,lw=2,label='$\\delta=0.025$: las horas responden')
ax2.plot(range(len(h1)),h1,color=RUST,lw=2,ls='--',label='$\\delta=1$: horas $\\approx 0$')
ax2.axhline(0,color='0.6',lw=.7,ls=':'); ax2.set_xlabel('trimestres'); ax2.grid(alpha=.25)
ax2.set_title('Respuesta de las horas al choque de productividad',fontsize=11)
ax2.legend(fontsize=9,frameon=False); fig2.tight_layout(); fig2.savefig("handout/assets/irf_hours.pdf"); plt.close(fig2)
print("impacto niveles y,c,i,h:",*[round(b[v][0],6) for v in ['y','c','i','h']])
print("Dynare*sig       y,c,i,h:",round(0.838053*sig,6),round(0.263919*sig,6),round(0.574134*sig,6),round(0.143114*sig,6))
print("h(delta=1) primeros 3:",np.round(h1[:3],8))
print("assets:",os.listdir("handout/assets"))
